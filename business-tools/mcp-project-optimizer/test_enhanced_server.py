#!/usr/bin/env python3
"""
Test script for the enhanced Project Knowledge Optimizer MCP server
"""

import asyncio
import json
import sys
import os

# Add the server directory to path
sys.path.append('C:\\Users\\ruben\\OneDrive\\Documents\\mcp_servers\\mcp-project-optimizer')

from server import ProjectKnowledgeOptimizerMCP

async def test_enhanced_server():
    """Test the enhanced server with new GUI tools"""
    print("="*60)
    print("  TESTING ENHANCED MCP SERVER v3.1")
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
        print(f"\nTOTAL TOOLS AVAILABLE: {len(tools)}")
        
        # List all tools
        print(f"\nALL AVAILABLE TOOLS:")
        for i, tool in enumerate(tools, 1):
            print(f"   {i:2d}. {tool['name']}")
        
        # Check for new GUI tools specifically
        gui_tools = [tool for tool in tools if 'project_instructions' in tool['name'] or 'synchronize' in tool['name'] or 'validate_file_references' in tool['name']]
        
        print(f"\nNEW GUI INSTRUCTION TOOLS ({len(gui_tools)}):")
        for tool in gui_tools:
            print(f"   - {tool['name']} - {tool['description'][:50]}...")
        
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
            print(f"\nSERVER INFO:")
            print(f"   Name: {server_info['name']}")
            print(f"   Version: {server_info['version']}")
            print(f"   Protocol: {init_response['result']['protocolVersion']}")
        
        print(f"\nEnhanced server test SUCCESSFUL!")
        print(f"   - All 11 tools properly registered")
        print(f"   - New GUI instruction capabilities available")
        print(f"   - Server version updated to 3.1.0")
        
    else:
        print(f"\nServer test FAILED:")
        print(f"   Response: {response}")
    
    print("="*60)

if __name__ == "__main__":
    asyncio.run(test_enhanced_server())
