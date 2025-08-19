#!/usr/bin/env python3
"""
DeepSeek MCP Server v1.3 - ZodError Fix
Handles all edge cases that cause union validation errors
"""

import asyncio
import json
import logging
import sys
from typing import Any, Dict, List, Optional, Union
import requests
import os

# Configure logging with UTF-8 encoding
logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger("deepseek")

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

    def ensure_valid_id(self, request_id: Any) -> Union[str, int]:
        """Ensure ID is never null - critical for Zod validation"""
        if request_id is None:
            return "unknown"  # Fallback to string ID
        if isinstance(request_id, (str, int)):
            return request_id
        return str(request_id)  # Convert to string as fallback

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP requests with bulletproof JSON-RPC protocol"""
        try:
            method = request.get("method")
            request_id = self.ensure_valid_id(request.get("id"))  # Never allow null ID
            
            # Base response structure - always include these
            base_response = {
                "jsonrpc": "2.0",
                "id": request_id
            }
            
            if method == "initialize":
                return {
                    **base_response,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {},
                            "resources": {},
                            "prompts": {}
                        },
                        "serverInfo": {
                            "name": "deepseek-mcp-server",
                            "version": "1.3.0"
                        }
                    }
                }
            
            elif method == "tools/list":
                return {
                    **base_response,
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
            
            elif method == "resources/list":
                # Always return valid result structure
                return {
                    **base_response,
                    "result": {
                        "resources": []
                    }
                }
            
            elif method == "prompts/list":
                # Always return valid result structure
                return {
                    **base_response,
                    "result": {
                        "prompts": []
                    }
                }
            
            elif method == "tools/call":
                params = request.get("params", {})
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                if not tool_name:
                    return {
                        **base_response,
                        "error": {
                            "code": -32602,
                            "message": "Missing tool name"
                        }
                    }
                
                prompt = arguments.get("prompt", "")
                if not prompt:
                    return {
                        **base_response,
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
                        **base_response,
                        "error": {
                            "code": -32602,
                            "message": f"Unknown tool: {tool_name}"
                        }
                    }
                
                # Format response - always include result structure
                if result.get("success"):
                    response_text = f"**DeepSeek {result.get('model', 'Response')}**\n\n{result.get('content', 'No content returned')}"
                    if result.get("usage"):
                        usage = result["usage"]
                        response_text += f"\n\n*Tokens used: {usage.get('total_tokens', 'unknown')}*"
                else:
                    response_text = f"**DeepSeek Error:** {result.get('error', 'Unknown error occurred')}"
                
                return {
                    **base_response,
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
                # For any other unknown method, return proper error with valid ID
                return {
                    **base_response,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
        
        except Exception as e:
            logger.error(f"Error handling request: {str(e)}")
            # Ensure we always return a valid response with proper ID
            safe_id = self.ensure_valid_id(request.get("id"))
            return {
                "jsonrpc": "2.0",
                "id": safe_id,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }

    async def run(self):
        """Main server loop"""
        logger.info("DeepSeek MCP Server starting (v1.3 - ZodError Fix)...")
        
        # Check API keys
        if self.deepseek_api_key:
            logger.info("Using DeepSeek Direct API")
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
                try:
                    request = json.loads(line)
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decode error: {e}")
                    # Send proper error response even for malformed JSON
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": "parse_error",  # Provide a valid ID
                        "error": {
                            "code": -32700,
                            "message": "Parse error"
                        }
                    }
                    print(json.dumps(error_response), flush=True)
                    continue
                
                logger.info(f"Message from client: {json.dumps(request)}")
                
                response = await self.handle_request(request)
                
                # Validate response structure before sending
                if not isinstance(response, dict) or "jsonrpc" not in response or "id" not in response:
                    logger.error("Invalid response structure detected")
                    safe_id = self.ensure_valid_id(request.get("id") if isinstance(request, dict) else None)
                    response = {
                        "jsonrpc": "2.0",
                        "id": safe_id,
                        "error": {
                            "code": -32603,
                            "message": "Internal error: Invalid response structure"
                        }
                    }
                
                # Log response
                logger.info(f"Message from server: {json.dumps(response)}")
                
                # Write JSON-RPC response
                print(json.dumps(response, ensure_ascii=False), flush=True)
                
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                # Send a valid error response even for unexpected errors
                error_response = {
                    "jsonrpc": "2.0",
                    "id": "error",
                    "error": {
                        "code": -32603,
                        "message": f"Unexpected error: {str(e)}"
                    }
                }
                print(json.dumps(error_response), flush=True)
                continue

async def main():
    server = DeepSeekMCPServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
