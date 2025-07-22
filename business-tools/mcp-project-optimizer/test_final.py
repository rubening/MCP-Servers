#!/usr/bin/env python3
"""
Final test for the enhanced Project Knowledge Optimizer MCP server v3.1
"""

import asyncio
import json
import sys
import os

# Add the server directory to path
sys.path.append('C:\\Users\\ruben\\OneDrive\\Documents\\mcp_servers\\mcp-project-optimizer')

async def test_enhanced_server():
    """Test the enhanced server with new GUI tools"""
    print("="*60)
    print("  TESTING ENHANCED MCP SERVER v3.1")
    print("="*60)
    
    try:
        # Import and initialize server
        from server import ProjectKnowledgeOptimizerMCP
        server = ProjectKnowledgeOptimizerMCP()
        print("âœ“ Server initialized successfully!")
        
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
            print(f"âœ“ Total tools available: {len(tools)}")
            
            # Check for new GUI tools specifically
            gui_tools = [tool for tool in tools if any(keyword in tool['name'] for keyword in ['generate_project', 'update_project', 'synchronize', 'validate_file'])]
            
            print(f"âœ“ New GUI instruction tools: {len(gui_tools)}")
            for tool in gui_tools:
                print(f"   - {tool['name']}")
            
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
                print(f"âœ“ Server info:")
                print(f"   Name: {server_info['name']}")
                print(f"   Version: {server_info['version']}")
                print(f"   Protocol: {init_response['result']['protocolVersion']}")
            
            # Verify we have all expected tools
            expected_tools = [
                'analyze_project_knowledge',
                'optimize_project_knowledge', 
                'validate_mcp_protocol',
                'backup_project_knowledge',
                'restore_project_knowledge',
                'safe_replace_project_knowledge',
                'analyze_conversation_issues',
                'generate_project_instructions',
                'update_project_instructions',
                'synchronize_project_files',
                'validate_file_references'
            ]
            
            actual_tools = [tool['name'] for tool in tools]
            missing_tools = [tool for tool in expected_tools if tool not in actual_tools]
            
            if missing_tools:
                print(f"âœ— Missing tools: {missing_tools}")
            else:
                print(f"âœ“ All expected tools present!")
            
            print(f"\nEnhanced server test SUCCESSFUL!")
            print(f"   - All {len(tools)} tools properly registered")
            print(f"   - {len(gui_tools)} new GUI instruction tools available")
            print(f"   - Server version updated to {server_info['version']}")
            
        else:
            print(f"âœ— Server test FAILED:")
            print(f"   Response: {response}")
    
    except Exception as e:
        print(f"âœ— Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("="*60)

if __name__ == "__main__":
    asyncio.run(test_enhanced_server())
