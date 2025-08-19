#!/usr/bin/env python3
"""
DeepSeek MCP Server - Fixed to use Direct API
Prioritizes working DeepSeek Direct API over broken OpenRouter
"""

import asyncio
import json
import logging
import sys
from typing import Any, Dict, List, Optional
import requests
import os

# Configure logging with UTF-8 encoding
logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)

class DeepSeekMCPServer:
    def __init__(self):
        # Get API keys from environment
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        self.openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
        
        # API endpoints
        self.deepseek_base_url = "https://api.deepseek.com"
        self.openrouter_base_url = "https://openrouter.ai/api/v1"

    def get_api_headers(self, use_openrouter=False):
        """Get API headers - prioritize DeepSeek Direct"""
        if use_openrouter and self.openrouter_api_key:
            return {
                "Authorization": f"Bearer {self.openrouter_api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://claude-desktop",
                "X-Title": "Claude Desktop DeepSeek MCP"
            }
        elif self.deepseek_api_key:
            return {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json"
            }
        else:
            raise ValueError("No API key configured")

    def call_deepseek_api(self, prompt: str, model: str = "deepseek-r1") -> Dict[str, Any]:
        """Call DeepSeek - prioritize direct API which is working"""
        try:
            # ALWAYS use DeepSeek Direct API first (it's working!)
            if self.deepseek_api_key:
                url = f"{self.deepseek_base_url}/v1/chat/completions"
                # Map model names
                if model == "deepseek-r1":
                    model_name = "deepseek-reasoner"
                else:
                    model_name = "deepseek-chat"
                headers = self.get_api_headers(use_openrouter=False)
                
            # Fallback to OpenRouter only if no DeepSeek key
            elif self.openrouter_api_key:
                url = f"{self.openrouter_base_url}/chat/completions"
                model_name = f"deepseek/{model}"
                headers = self.get_api_headers(use_openrouter=True)
            else:
                return {
                    "success": False,
                    "error": "No API key configured"
                }

            payload = {
                "model": model_name,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.2 if "reasoner" in model_name or "r1" in model else 0.7,
                "max_tokens": 4000,
                "stream": False
            }

            logger.info(f"Calling DeepSeek API: {model_name}")
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                
                # Handle encoding issues with emojis
                try:
                    # Try to encode as UTF-8 first
                    content = content.encode('utf-8').decode('utf-8')
                except:
                    # Fallback: remove problematic characters
                    content = content.encode('ascii', 'ignore').decode('ascii')
                
                return {
                    "success": True,
                    "content": content,
                    "model": model_name,
                    "usage": result.get("usage", {})
                }
            else:
                logger.error(f"API Error: {response.status_code} - {response.text}")
                return {
                    "success": False,
                    "error": f"API Error {response.status_code}: {response.text[:200]}"
                }

        except Exception as e:
            logger.error(f"Exception: {str(e)}")
            return {
                "success": False,
                "error": f"Exception: {str(e)}"
            }

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP requests with proper JSON-RPC protocol"""
        try:
            method = request.get("method")
            request_id = request.get("id")
            
            if method == "initialize":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "deepseek-mcp-server",
                            "version": "1.1.0"
                        }
                    }
                }
            
            elif method == "tools/list":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "tools": [
                            {
                                "name": "deepseek_reasoning",
                                "description": "Advanced reasoning using DeepSeek R1 for complex analysis and problem-solving",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "prompt": {
                                            "type": "string",
                                            "description": "The complex question or problem requiring deep reasoning"
                                        }
                                    },
                                    "required": ["prompt"],
                                    "additionalProperties": False
                                }
                            },
                            {
                                "name": "deepseek_chat",
                                "description": "General conversation using DeepSeek Chat for questions and discussions",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "prompt": {
                                            "type": "string",
                                            "description": "The question or topic for discussion"
                                        }
                                    },
                                    "required": ["prompt"],
                                    "additionalProperties": False
                                }
                            }
                        ]
                    }
                }
            
            elif method == "tools/call":
                params = request.get("params", {})
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                if not tool_name:
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32602,
                            "message": "Missing tool name"
                        }
                    }
                
                prompt = arguments.get("prompt", "")
                if not prompt:
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32602,
                            "message": "Missing prompt argument"
                        }
                    }
                
                # Call appropriate model
                if tool_name == "deepseek_reasoning":
                    result = self.call_deepseek_api(prompt, "deepseek-r1")
                elif tool_name == "deepseek_chat":
                    result = self.call_deepseek_api(prompt, "deepseek-chat")
                else:
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32602,
                            "message": f"Unknown tool: {tool_name}"
                        }
                    }
                
                # Format response
                if result.get("success"):
                    response_text = f"**DeepSeek {result.get('model', 'Response')}**\n\n{result.get('content', 'No content returned')}"
                    if result.get("usage"):
                        usage = result["usage"]
                        response_text += f"\n\n*Tokens used: {usage.get('total_tokens', 'unknown')}*"
                else:
                    response_text = f"**DeepSeek Error:** {result.get('error', 'Unknown error occurred')}"
                
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": response_text
                            }
                        ]
                    }
                }
            
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
        
        except Exception as e:
            logger.error(f"Error handling request: {str(e)}")
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }

    async def run(self):
        """Main server loop"""
        logger.info("DeepSeek MCP Server starting (v1.1 - Direct API Priority)...")
        
        # Check API keys
        if self.deepseek_api_key:
            logger.info("Using DeepSeek Direct API (WORKING)")
        elif self.openrouter_api_key:
            logger.info("Using OpenRouter API (fallback)")
        else:
            logger.error("No API key found. Set DEEPSEEK_API_KEY or OPENROUTER_API_KEY")
            return
        
        # Set encoding for stdin/stdout
        if sys.platform == "win32":
            import io
            sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        
        while True:
            try:
                # Read from stdin (async)
                line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                if not line:
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                # Parse JSON-RPC request
                request = json.loads(line)
                response = await self.handle_request(request)
                
                # Write JSON-RPC response
                print(json.dumps(response, ensure_ascii=False), flush=True)
                
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
                # Send error response
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": "Parse error"
                    }
                }
                print(json.dumps(error_response), flush=True)
                continue
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                continue

async def main():
    server = DeepSeekMCPServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
