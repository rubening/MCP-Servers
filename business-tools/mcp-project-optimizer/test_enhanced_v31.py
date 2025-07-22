#!/usr/bin/env python3
"""
Test script for the enhanced Project Knowledge Optimizer MCP server v3.1
Tests all 11 tools including the new GUI instruction capabilities
"""

import asyncio
import json
import sys
import os

# Add the server directory to path
sys.path.append('C:\\Users\\ruben\\OneDrive\\Documents\\mcp_servers\\mcp-project-optimizer')

from server import ProjectKnowledgeOptimizerMCP

async def test_enhanced_server_v31():
    """Test the enhanced server v3.1 with all 11 tools"""
    print("="*70)
    print("  TESTING ENHANCED MCP SERVER v3.1 - ALL TOOLS")
    print("="*70)
    
    # Initialize server
    server = ProjectKnowledgeOptimizerMCP()
    
    # Test server initialization
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {}
    }
    
    init_response = await server.handle_request(init_request)
    
    if "result" in init_response:
        server_info = init_response["result"]["serverInfo"]
        print(f"âœ“ SERVER INITIALIZATION:")
        print(f"   Name: {server_info['name']}")
        print(f"   Version: {server_info['version']}")
        print(f"   Protocol: {init_response['result']['protocolVersion']}")
        print()
    else:
        print("âœ— Server initialization FAILED")
        return
    
    # Test tools/list to see all available tools
    request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    
    response = await server.handle_request(request)
    
    if "result" in response and "tools" in response["result"]:
        tools = response["result"]["tools"]
        
        print(f"âœ“ TOOLS REGISTRATION:")
        print(f"   Total Tools Available: {len(tools)}")
        
        # Expected tools (11 total)
        expected_tools = [
            "analyze_project_knowledge",
            "optimize_project_knowledge", 
            "validate_mcp_protocol",
            "backup_project_knowledge",
            "restore_project_knowledge",
            "safe_replace_project_knowledge",
            "analyze_conversation_issues",
            "generate_project_instructions",    # NEW
            "update_project_instructions",      # NEW
            "synchronize_project_files",       # NEW
            "validate_file_references"         # NEW
        ]
        
        # List all tools and check against expected
        print(f"   ALL REGISTERED TOOLS:")
        found_tools = [tool['name'] for tool in tools]
        
        for i, tool in enumerate(tools, 1):
            status = "âœ“" if tool['name'] in expected_tools else "?"
            print(f"      {i:2d}. {status} {tool['name']}")
        
        # Check for missing expected tools
        missing_tools = set(expected_tools) - set(found_tools)
        extra_tools = set(found_tools) - set(expected_tools)
        
        print()
        print(f"âœ“ TOOL VALIDATION:")
        print(f"   Expected Tools: {len(expected_tools)}")
        print(f"   Found Tools: {len(found_tools)}")
        print(f"   Missing Tools: {len(missing_tools)}")
        print(f"   Extra Tools: {len(extra_tools)}")
        
        if missing_tools:
            print(f"   âœ— MISSING: {', '.join(missing_tools)}")
        
        if extra_tools:
            print(f"   ? EXTRA: {', '.join(extra_tools)}")
        
        # Categorize tools
        original_tools = [
            "analyze_project_knowledge", "optimize_project_knowledge", 
            "validate_mcp_protocol", "backup_project_knowledge",
            "restore_project_knowledge", "safe_replace_project_knowledge",
            "analyze_conversation_issues"
        ]
        
        new_gui_tools = [
            "generate_project_instructions", "update_project_instructions",
            "synchronize_project_files", "validate_file_references"
        ]
        
        found_original = [t for t in found_tools if t in original_tools]
        found_new = [t for t in found_tools if t in new_gui_tools]
        
        print()
        print(f"âœ“ TOOL CATEGORIES:")
        print(f"   Original Tools: {len(found_original)}/{len(original_tools)}")
        for tool in found_original:
            print(f"      âœ“ {tool}")
        
        print(f"   New GUI Tools: {len(found_new)}/{len(new_gui_tools)}")
        for tool in found_new:
            print(f"      âœ“ {tool}")
        
        # Test a few key tool schemas
        print()
        print(f"âœ“ TOOL SCHEMA VALIDATION:")
        
        schema_tests = [
            "analyze_project_knowledge",
            "generate_project_instructions",
            "validate_file_references"
        ]
        
        for tool_name in schema_tests:
            tool_def = next((t for t in tools if t['name'] == tool_name), None)
            if tool_def:
                schema = tool_def.get('inputSchema', {})
                required = schema.get('required', [])
                properties = schema.get('properties', {})
                
                print(f"   âœ“ {tool_name}:")
                print(f"      Required params: {len(required)}")
                print(f"      Total params: {len(properties)}")
                print(f"      Schema valid: {'Yes' if schema else 'No'}")
            else:
                print(f"   âœ— {tool_name}: Not found")
        
        # Overall assessment
        print()
        print(f"âœ“ OVERALL ASSESSMENT:")
        
        all_expected_found = len(missing_tools) == 0
        version_correct = server_info.get('version') == '3.1.0'
        tool_count_correct = len(found_tools) == 11
        
        print(f"   All Expected Tools: {'âœ“ Yes' if all_expected_found else 'âœ— No'}")
        print(f"   Correct Version: {'âœ“ Yes' if version_correct else 'âœ— No'}")
        print(f"   Tool Count (11): {'âœ“ Yes' if tool_count_correct else 'âœ— No'}")
        
        if all_expected_found and version_correct and tool_count_correct:
            print(f"   Status: âœ“ SUCCESS - Enhanced server v3.1 fully functional!")
        else:
            print(f"   Status: âœ— ISSUES DETECTED - Review failed checks above")
        
    else:
        print("âœ— Tools list retrieval FAILED:")
        print(f"   Response: {response}")
    
    print("="*70)

if __name__ == "__main__":
    asyncio.run(test_enhanced_server_v31())
