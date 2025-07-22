#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ErrorCode,
  ListToolsRequestSchema,
  McpError,
} from "@modelcontextprotocol/sdk/types.js";
import axios from 'axios';
import * as cheerio from 'cheerio';

class WebSearchMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: "web-search-mcp-server",
        version: "1.0.0",
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupToolHandlers();
  }

  setupToolHandlers() {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: "web_search",
          description: "Search the web for information on any topic",
          inputSchema: {
            type: "object",
            properties: {
              query: {
                type: "string",
                description: "Search query to find information about"
              },
              max_results: {
                type: "number",
                description: "Maximum number of results to return (default: 10)",
                default: 10
              },
              region: {
                type: "string",
                description: "Region for search (us-en, uk-en, etc.)",
                default: "us-en"
              }
            },
            required: ["query"]
          }
        },
        {
          name: "fetch_webpage",
          description: "Fetch and extract content from a specific webpage",
          inputSchema: {
            type: "object",
            properties: {
              url: {
                type: "string",
                description: "URL of the webpage to fetch"
              },
              extract_text_only: {
                type: "boolean",
                description: "Extract only text content, no HTML",
                default: true
              }
            },
            required: ["url"]
          }
        },
        {
          name: "search_news",
          description: "Search for recent news articles on a topic",
          inputSchema: {
            type: "object",
            properties: {
              query: {
                type: "string",
                description: "News topic to search for"
              },
              max_results: {
                type: "number",
                description: "Maximum number of news articles to return",
                default: 5
              },
              time_range: {
                type: "string",
                description: "Time range for news (day, week, month)",
                default: "week"
              }
            },
            required: ["query"]
          }
        },
        {
          name: "search_images",
          description: "Search for images related to a topic",
          inputSchema: {
            type: "object",
            properties: {
              query: {
                type: "string",
                description: "Image search query"
              },
              max_results: {
                type: "number",
                description: "Maximum number of images to return",
                default: 10
              },
              size: {
                type: "string",
                description: "Image size filter (small, medium, large)",
                default: "medium"
              }
            },
            required: ["query"]
          }
        }
      ]
    }));

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case "web_search":
            return await this.webSearch(args);
          case "fetch_webpage":
            return await this.fetchWebpage(args);
          case "search_news":
            return await this.searchNews(args);
          case "search_images":
            return await this.searchImages(args);
          default:
            throw new McpError(
              ErrorCode.MethodNotFound,
              `Unknown tool: ${name}`
            );
        }
      } catch (error) {
        return {
          content: [
            {
              type: "text",
              text: `Error: ${error.message}`
            }
          ]
        };
      }
    });
  }

  async webSearch(args) {
    const { query, max_results = 10, region = "us-en" } = args;
    
    try {
      // Use DuckDuckGo instant answers API
      const searchUrl = `https://api.duckduckgo.com/?q=${encodeURIComponent(query)}&format=json&no_html=1&skip_disambig=1`;
      
      const response = await axios.get(searchUrl, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
      });

      const data = response.data;
      const results = [];

      // Add instant answer if available
      if (data.AbstractText) {
        results.push({
          title: data.Heading || 'Instant Answer',
          snippet: data.AbstractText,
          url: data.AbstractURL || '',
          source: data.AbstractSource || 'DuckDuckGo'
        });
      }

      // Add related topics
      if (data.RelatedTopics && data.RelatedTopics.length > 0) {
        data.RelatedTopics.slice(0, max_results - 1).forEach(topic => {
          if (topic.Text) {
            results.push({
              title: topic.Text.split(' - ')[0] || 'Related Topic',
              snippet: topic.Text,
              url: topic.FirstURL || '',
              source: 'DuckDuckGo Related'
            });
          }
        });
      }

      // Add definition if available
      if (data.Definition) {
        results.push({
          title: 'Definition',
          snippet: data.Definition,
          url: data.DefinitionURL || '',
          source: data.DefinitionSource || 'Dictionary'
        });
      }

      // Fallback to HTML search if no results
      if (results.length === 0) {
        return await this.htmlSearch(query, max_results);
      }

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({
              query,
              total_results: results.length,
              results: results.slice(0, max_results)
            }, null, 2)
          }
        ]
      };

    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Error searching web: ${error.message}`
          }
        ]
      };
    }
  }

  async htmlSearch(query, maxResults = 10) {
    try {
      // Fallback HTML search using DuckDuckGo's HTML interface
      const searchUrl = `https://html.duckduckgo.com/html/?q=${encodeURIComponent(query)}`;
      
      const response = await axios.get(searchUrl, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
      });

      const $ = cheerio.load(response.data);
      const results = [];

      $('.result').each((index, element) => {
        if (index >= maxResults) return false;

        const titleEl = $(element).find('.result__title a');
        const snippetEl = $(element).find('.result__snippet');
        const urlEl = $(element).find('.result__url');

        const title = titleEl.text().trim();
        const snippet = snippetEl.text().trim();
        const url = titleEl.attr('href') || '';

        if (title && snippet) {
          results.push({
            title,
            snippet,
            url: url.startsWith('//') ? 'https:' + url : url,
            source: 'Web Search'
          });
        }
      });

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({
              query,
              total_results: results.length,
              results
            }, null, 2)
          }
        ]
      };

    } catch (error) {
      throw new Error(`HTML search failed: ${error.message}`);
    }
  }

  async fetchWebpage(args) {
    const { url, extract_text_only = true } = args;
    
    try {
      const response = await axios.get(url, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        },
        timeout: 10000
      });

      const $ = cheerio.load(response.data);
      
      // Remove script and style elements
      $('script, style, nav, footer, aside').remove();

      let content;
      if (extract_text_only) {
        // Extract main content
        const mainContent = $('main, article, .content, .post, .entry').first();
        if (mainContent.length > 0) {
          content = mainContent.text().trim();
        } else {
          content = $('body').text().trim();
        }
        
        // Clean up whitespace
        content = content.replace(/\s+/g, ' ').trim();
        
        // Limit content length
        if (content.length > 5000) {
          content = content.substring(0, 5000) + '...';
        }
      } else {
        content = $.html();
      }

      const title = $('title').text().trim() || 'No title';
      const description = $('meta[name="description"]').attr('content') || '';

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({
              url,
              title,
              description,
              content,
              length: content.length,
              extracted_at: new Date().toISOString()
            }, null, 2)
          }
        ]
      };

    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Error fetching webpage: ${error.message}`
          }
        ]
      };
    }
  }

  async searchNews(args) {
    const { query, max_results = 5, time_range = "week" } = args;
    
    try {
      // Search for news using DuckDuckGo with news-specific query
      const newsQuery = `${query} news site:news.google.com OR site:reuters.com OR site:ap.org OR site:bbc.com`;
      return await this.webSearch({
        query: newsQuery,
        max_results,
        region: "us-en"
      });

    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Error searching news: ${error.message}`
          }
        ]
      };
    }
  }

  async searchImages(args) {
    const { query, max_results = 10, size = "medium" } = args;
    
    try {
      // Use DuckDuckGo image search
      const imageUrl = `https://duckduckgo.com/?q=${encodeURIComponent(query)}&t=h_&iax=images&ia=images`;
      
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({
              query,
              search_url: imageUrl,
              message: "Image search initiated. Visit the URL above to view results.",
              note: "Direct image URLs cannot be provided due to API limitations"
            }, null, 2)
          }
        ]
      };

    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Error searching images: ${error.message}`
          }
        ]
      };
    }
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error("Web Search MCP server running on stdio");
  }
}

const server = new WebSearchMCPServer();
server.run().catch(console.error);
