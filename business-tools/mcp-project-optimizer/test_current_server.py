#!/usr/bin/env python3
"""
Test script for the current Project Knowledge Optimizer MCP server
"""

import asyncio
import json
import sys
import os

# Add the server directory to path
sys.path.append('C:\\Users\\ruben\\OneDrive\\Documents\\mcp_servers\\mcp-project-optimizer')

from server import ProjectKnowledgeOptimizerMCP

async def test_current_server():
    """Test the current server with existing tools"""
    print("="*60)
    print("  TESTING CURRENT MCP SERVER v3.0")
    print("="*60)
    
    # Initialize server
    server = ProjectKnowledgeOptimizerMCP()
    
    # Test tools/list to see all available tools
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
        "params": {}
    }
    
    response = await server.handle_request(request)
    
    if "result" in response and "tools" in response["result"]:
        tools = response["result"]["tools"]
        print(f"TOTAL TOOLS AVAILABLE: {len(tools)}")
        
        # List all tools
        print(f"ALL AVAILABLE TOOLS:")
        for i, tool in enumerate(tools, 1):
            print(f"   {i:2d}. {tool['name']}")
        
        # Test server info
        init_request = {
            "jsonrpc": "2.0", 
            "id": 2,
            "method": "initialize",
            "params": {}
        }
        
        init_response = await server.handle_request(init_request)
        if "result" in init_response:
            server_info = init_response["result"]["serverInfo"]
            print(f"SERVER INFO:")
            print(f"   Name: {server_info['name']}")
            print(f"   Version: {server_info['version']}")
            print(f"   Protocol: {init_response['result']['protocolVersion']}")
        
        print(f"Current server test SUCCESSFUL!")
        print(f"   - All {len(tools)} tools properly registered")
        print(f"   - Server version {server_info['version']}")
        print(f"   - MCP protocol {init_response['result']['protocolVersion']}")
        
    else:
        print(f"Server test FAILED:")
        print(f"   Response: {response}")
    
    print("="*60)

if __name__ == "__main__":
    asyncio.run(test_current_server())
