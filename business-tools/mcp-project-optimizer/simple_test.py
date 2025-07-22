#!/usr/bin/env python3
"""
Simple import test for the server
"""

import sys
import os

print("Starting import test...")

sys.path.append('C:\\Users\\ruben\\OneDrive\\Documents\\mcp_servers\\mcp-project-optimizer')

try:
    print("Importing server...")
    from server import ProjectKnowledgeOptimizerMCP
    print("âœ“ Server imported successfully!")
    
    print("Creating server instance...")
    server = ProjectKnowledgeOptimizerMCP()
    print("âœ“ Server instance created!")
    
    print("Testing async method (simulate tools list)...")
    import asyncio
    
    async def test_tools():
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
        
        response = await server.handle_request(request)
        
        if "result" in response and "tools" in response["result"]:
            tools = response["result"]["tools"]
            print(f"âœ“ Tools retrieved: {len(tools)} tools found")
            
            # Show first few tools
            for i, tool in enumerate(tools[:5], 1):
                print(f"   {i}. {tool['name']}")
            
            if len(tools) > 5:
                print(f"   ... and {len(tools) - 5} more")
            
            return tools
        else:
            print(f"âœ— Failed to get tools: {response}")
            return []
    
    tools = asyncio.run(test_tools())
    
    print(f"\nSUMMARY:")
    print(f"âœ“ Import: Success")
    print(f"âœ“ Instance: Success") 
    print(f"âœ“ Tools Count: {len(tools)}")
    print(f"âœ“ Expected: 11 tools")
    print(f"âœ“ Status: {'SUCCESS' if len(tools) == 11 else 'PARTIAL'}")
    
except Exception as e:
    print(f"âœ— ERROR: {str(e)}")
    import traceback
    traceback.print_exc()

print("Test completed.")
