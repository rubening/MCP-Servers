# Web Search MCP Server

## What This Does

This MCP server provides comprehensive web search capabilities:

- **Web Search**: Search the internet for any topic
- **Webpage Fetching**: Extract content from specific URLs
- **News Search**: Find recent news articles
- **Image Search**: Search for images (provides search URLs)

## Installation

```powershell
cd "C:\Users\ruben\Claude Tools\web-search-mcp-server"
npm install
```

## Available Tools

### 1. Web Search
Search the internet for information on any topic.

```json
{
  "tool": "web_search",
  "parameters": {
    "query": "best pizza restaurants Chicago",
    "max_results": 10,
    "region": "us-en"
  }
}
```

### 2. Fetch Webpage
Extract content from a specific URL.

```json
{
  "tool": "fetch_webpage", 
  "parameters": {
    "url": "https://example.com/article",
    "extract_text_only": true
  }
}
```

### 3. Search News
Find recent news articles on a topic.

```json
{
  "tool": "search_news",
  "parameters": {
    "query": "artificial intelligence breakthrough",
    "max_results": 5,
    "time_range": "week"
  }
}
```

### 4. Search Images
Search for images related to a topic.

```json
{
  "tool": "search_images",
  "parameters": {
    "query": "Chicago skyline",
    "max_results": 10,
    "size": "large"
  }
}
```

## Configuration for Claude Desktop

Add this to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "web-search": {
      "command": "node",
      "args": ["C:\\Users\\ruben\\Claude Tools\\web-search-mcp-server\\index.js"],
      "cwd": "C:\\Users\\ruben\\Claude Tools\\web-search-mcp-server"
    }
  }
}
```

## Example Usage

- "Search the web for the best restaurants in Miami"
- "Find recent news about Tesla stock price"
- "Get the content from this article URL"
- "Search for images of the Golden Gate Bridge"

## Features

- **No API Keys Required**: Uses DuckDuckGo which doesn't require registration
- **Content Extraction**: Intelligently extracts main content from webpages
- **News Filtering**: Searches reliable news sources
- **Rate Limiting**: Built-in delays to respect website policies
- **Error Handling**: Graceful handling of network issues

## Note

This server uses publicly available search engines and respects robots.txt files and rate limits. It's designed for legitimate research and information gathering purposes.
