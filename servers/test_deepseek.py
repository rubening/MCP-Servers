#!/usr/bin/env python3
"""
Test script to debug DeepSeek MCP server JSON-RPC protocol issues
"""

import asyncio
import json
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from deepseek_mcp_fixed import DeepSeekMCPServer

async def test_deepseek_server():
    """Test DeepSeek server responses to identify JSON-RPC issues"""
    
    print("=== DeepSeek MCP Server Debug Test ===\n")
    
    server = DeepSeekMCPServer()
    
    # Test 1: Initialize request
    print("Test 1: Initialize Request")
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {}
        }
    }
    
    response = await server.handle_request(init_request)
    print(f"Request: {json.dumps(init_request, indent=2)}")
    print(f"Response: {json.dumps(response, indent=2)}")
    print()
    
    # Test 2: Tools list request  
    print("Test 2: Tools List Request")
    tools_request = {
        "jsonrpc": "2.0", 
        "id": 2,
        "method": "tools/list"
    }
    
    response = await server.handle_request(tools_request)
    print(f"Request: {json.dumps(tools_request, indent=2)}")
    print(f"Response: {json.dumps(response, indent=2)}")
    print()
    
    # Test 3: Simple tool call
    print("Test 3: Simple Tool Call")
    tool_request = {
        "jsonrpc": "2.0",
        "id": 3, 
        "method": "tools/call",
        "params": {
            "name": "deepseek_chat",
            "arguments": {
                "prompt": "Hello, this is a test message. Please respond briefly."
            }
        }
    }
    
    response = await server.handle_request(tool_request)
    print(f"Request: {json.dumps(tool_request, indent=2)}")
    print(f"Response: {json.dumps(response, indent=2)}")
    print()
    
    # Validation checks
    print("=== JSON-RPC Protocol Validation ===")
    responses = [
        await server.handle_request(init_request),
        await server.handle_request(tools_request), 
        await server.handle_request(tool_request)
    ]
    
    for i, resp in enumerate(responses, 1):
        print(f"\nResponse {i} Validation:")
        
        # Check required fields
        if "jsonrpc" not in resp:
            print("ERROR: Missing 'jsonrpc' field")
        elif resp["jsonrpc"] != "2.0":
            print(f"ERROR: Invalid jsonrpc version: {resp['jsonrpc']}")
        else:
            print("OK: jsonrpc field correct")
            
        if "id" not in resp:
            print("ERROR: Missing 'id' field")
        elif resp["id"] is None:
            print("ERROR: 'id' field is null")
        else:
            print(f"OK: id field present: {resp['id']}")
            
        if "result" in resp and "error" in resp:
            print("ERROR: Both 'result' and 'error' present")
        elif "result" not in resp and "error" not in resp:
            print("ERROR: Neither 'result' nor 'error' present")
        else:
            print("OK: Proper result/error structure")

if __name__ == "__main__":
    asyncio.run(test_deepseek_server())
