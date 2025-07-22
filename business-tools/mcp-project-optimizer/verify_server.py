#!/usr/bin/env python3
"""
Simple verification script for enhanced MCP server v3.1
"""

import asyncio
import sys
import os

sys.path.append('C:\\Users\\ruben\\OneDrive\\Documents\\mcp_servers\\mcp-project-optimizer')

async def verify_server():
    try:
        from server import ProjectKnowledgeOptimizerMCP
        
        server = ProjectKnowledgeOptimizerMCP()
        
        # Test initialization
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {}
        }
        
        init_response = await server.handle_request(init_request)
        
        # Test tools list
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        tools_response = await server.handle_request(tools_request)
        
        # Write results to file
        with open('server_verification.txt', 'w') as f:
            f.write("MCP Server v3.1 Verification Results\n")
            f.write("="*50 + "\n\n")
            
            if "result" in init_response:
                server_info = init_response["result"]["serverInfo"]
                f.write(f"Server Name: {server_info['name']}\n")
                f.write(f"Server Version: {server_info['version']}\n")
                f.write(f"Protocol Version: {init_response['result']['protocolVersion']}\n\n")
            
            if "result" in tools_response:
                tools = tools_response["result"]["tools"]
                f.write(f"Total Tools: {len(tools)}\n\n")
                
                f.write("All Tools:\n")
                for i, tool in enumerate(tools, 1):
                    f.write(f"  {i:2d}. {tool['name']}\n")
                
                # Check for new GUI tools
                gui_tools = [
                    "generate_project_instructions",
                    "update_project_instructions", 
                    "synchronize_project_files",
                    "validate_file_references"
                ]
                
                found_gui = [t['name'] for t in tools if t['name'] in gui_tools]
                f.write(f"\nNew GUI Tools Found: {len(found_gui)}/4\n")
                for tool in found_gui:
                    f.write(f"  âœ“ {tool}\n")
                
                f.write(f"\nVerification: {'SUCCESS' if len(tools) == 11 and len(found_gui) == 4 else 'FAILED'}\n")
            
            else:
                f.write("ERROR: Failed to get tools list\n")
        
        return True
        
    except Exception as e:
        with open('server_verification.txt', 'w') as f:
            f.write(f"ERROR: {str(e)}\n")
        return False

if __name__ == "__main__":
    result = asyncio.run(verify_server())
    print(f"Verification completed. Result written to server_verification.txt")
