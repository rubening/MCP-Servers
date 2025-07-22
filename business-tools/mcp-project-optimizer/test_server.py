#!/usr/bin/env python3
"""
Test script for the MCP Project Knowledge Optimizer Server

This script tests the basic functionality of the server to ensure
all tools are working correctly before integration with Claude Desktop.
"""

import asyncio
import json
import subprocess
import sys
import os
from pathlib import Path

# Add the server directory to the path
server_dir = Path(__file__).parent
sys.path.insert(0, str(server_dir))

# Import the server class
from server import ProjectKnowledgeOptimizerMCP


async def test_server_initialization():
    """Test that the server initializes correctly"""
    print("Testing server initialization...")
    
    try:
        mcp = ProjectKnowledgeOptimizerMCP()
        print("SUCCESS: Server initialized successfully")
        return True
    except Exception as e:
        print(f"ERROR: Server initialization failed: {e}")
        return False


async def test_mcp_protocol():
    """Test the MCP protocol methods"""
    print("\nTesting MCP protocol methods...")
    
    try:
        mcp = ProjectKnowledgeOptimizerMCP()
        
        # Test initialize method
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {}
        }
        
        response = await mcp.handle_request(init_request)
        
        if "result" in response:
            print("SUCCESS: Initialize method working")
            print(f"   Protocol Version: {response['result']['protocolVersion']}")
            print(f"   Server Info: {response['result']['serverInfo']['name']} v{response['result']['serverInfo']['version']}")
        else:
            print(f"ERROR: Initialize method failed: {response}")
            return False
        
        # Test tools/list method
        tools_request = {
            "jsonrpc": "2.0", 
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        response = await mcp.handle_request(tools_request)
        
        if "result" in response and "tools" in response["result"]:
            tools = response["result"]["tools"]
            print(f"SUCCESS: Tools list method working - {len(tools)} tools available:")
            for tool in tools:
                print(f"   - {tool['name']}: {tool['description'][:50]}...")
        else:
            print(f"ERROR: Tools list method failed: {response}")
            return False
            
        return True
        
    except Exception as e:
        print(f"ERROR: MCP protocol test failed: {e}")
        return False


async def test_analyze_tool():
    """Test the analyze_project_knowledge tool with a sample file"""
    print("\nTesting analyze_project_knowledge tool...")
    
    try:
        mcp = ProjectKnowledgeOptimizerMCP()
        
        # Create a sample project_knowledge.md file for testing
        test_file_path = server_dir / "test_sample.md"
        sample_content = """# Test Project

## Overview
This is a test project to verify the analyzer is working correctly.

## Technical Stack
- Python 3.11+
- MCP Protocol 2024-11-05
- FastAPI for web framework

## Requirements
- Must analyze document structure
- Should provide quality scores
- Need recommendations for improvement

## Current Issues
- File might be too short for optimal analysis
- May need more sections for better structure
"""
        
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(sample_content)
        
        # Test the analyze tool
        analyze_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "analyze_project_knowledge",
                "arguments": {
                    "file_path": str(test_file_path),
                    "detailed": False
                }
            }
        }
        
        response = await mcp.handle_request(analyze_request)
        
        if "result" in response and "content" in response["result"]:
            result_text = response["result"]["content"][0]["text"]
            if "OVERALL QUALITY SCORE" in result_text:
                print("SUCCESS: Analyze tool working correctly")
                
                # Extract score for verification
                import re
                score_match = re.search(r'OVERALL QUALITY SCORE: ([\d.]+)/100', result_text)
                if score_match:
                    score = float(score_match.group(1))
                    print(f"   Quality Score: {score}/100")
                    if 0 <= score <= 100:
                        print("   SUCCESS: Score in valid range")
                    else:
                        print("   WARNING: Score outside valid range")
            else:
                print("ERROR: Analyze tool response missing expected content")
                print(f"Response: {result_text[:200]}...")
                return False
        else:
            print(f"ERROR: Analyze tool failed: {response}")
            return False
        
        # Clean up test file
        test_file_path.unlink()
        return True
        
    except Exception as e:
        print(f"ERROR: Analyze tool test failed: {e}")
        return False


async def test_backup_tool():
    """Test the backup_project_knowledge tool"""
    print("\nTesting backup_project_knowledge tool...")
    
    try:
        mcp = ProjectKnowledgeOptimizerMCP()
        
        # Create a test file to backup
        test_file_path = server_dir / "test_backup_sample.md"
        sample_content = """# Backup Test Project

This is a test file for verifying the backup functionality works correctly.

## Features
- Versioned backups
- Metadata tracking
- Quality analysis inclusion
"""
        
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(sample_content)
        
        # Test the backup tool
        backup_request = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call", 
            "params": {
                "name": "backup_project_knowledge",
                "arguments": {
                    "file_path": str(test_file_path),
                    "backup_name": "test_backup",
                    "include_analysis": True
                }
            }
        }
        
        response = await mcp.handle_request(backup_request)
        
        if "result" in response and "content" in response["result"]:
            result_text = response["result"]["content"][0]["text"]
            if "Backup created successfully" in result_text:
                print("SUCCESS: Backup tool working correctly")
                
                # Extract backup ID for verification
                import re
                backup_match = re.search(r'Backup ID: ([^\n]+)', result_text)
                if backup_match:
                    backup_id = backup_match.group(1).strip()
                    print(f"   Backup ID: {backup_id}")
                    
                    # Verify backup directory was created
                    backup_dir = mcp.backup_dir / backup_id
                    if backup_dir.exists():
                        print("   SUCCESS: Backup directory created")
                        
                        # Check for backup files
                        backup_file = backup_dir / "project_knowledge.md"
                        metadata_file = backup_dir / "metadata.json"
                        
                        if backup_file.exists() and metadata_file.exists():
                            print("   SUCCESS: Backup files created correctly")
                        else:
                            print("   WARNING: Some backup files missing")
                    else:
                        print("   ERROR: Backup directory not created")
            else:
                print("ERROR: Backup tool response missing success indicator")
                print(f"Response: {result_text[:200]}...")
                return False
        else:
            print(f"ERROR: Backup tool failed: {response}")
            return False
        
        # Clean up test file
        test_file_path.unlink()
        return True
        
    except Exception as e:
        print(f"ERROR: Backup tool test failed: {e}")
        return False


async def test_validate_tool():
    """Test the validate_mcp_protocol tool"""
    print("\nTesting validate_mcp_protocol tool...")
    
    try:
        mcp = ProjectKnowledgeOptimizerMCP()
        
        # Test the validate tool
        validate_request = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {
                "name": "validate_mcp_protocol",
                "arguments": {
                    "check_server": True
                }
            }
        }
        
        response = await mcp.handle_request(validate_request)
        
        if "result" in response and "content" in response["result"]:
            result_text = response["result"]["content"][0]["text"]
            if "MCP PROTOCOL VALIDATION REPORT" in result_text:
                print("SUCCESS: Validate tool working correctly")
                
                # Check for key validation elements
                if "Protocol Version: 2024-11-05" in result_text:
                    print("   SUCCESS: Protocol version validation working")
                
                if "Server Info: project-knowledge-optimizer" in result_text:
                    print("   SUCCESS: Server info validation working")
                    
                if "TECHNICAL DISCOVERIES" in result_text:
                    print("   SUCCESS: Technical discoveries validation working")
                    
            else:
                print("ERROR: Validate tool response missing expected content")
                print(f"Response: {result_text[:200]}...")
                return False
        else:
            print(f"ERROR: Validate tool failed: {response}")
            return False
        
        return True
        
    except Exception as e:
        print(f"ERROR: Validate tool test failed: {e}")
        return False


async def main():
    """Run all tests"""
    print("="*60)
    print("  MCP PROJECT KNOWLEDGE OPTIMIZER - SERVER TESTS")
    print("="*60)
    
    tests = [
        ("Server Initialization", test_server_initialization),
        ("MCP Protocol", test_mcp_protocol), 
        ("Analyze Tool", test_analyze_tool),
        ("Backup Tool", test_backup_tool),
        ("Validate Tool", test_validate_tool)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nRunning {test_name} test...")
        try:
            if await test_func():
                passed += 1
                print(f"SUCCESS: {test_name} test PASSED")
            else:
                print(f"ERROR: {test_name} test FAILED")
        except Exception as e:
            print(f"ERROR: {test_name} test ERROR: {e}")
    
    print("\n" + "="*60)
    print(f"  TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("  ALL TESTS PASSED! Server is ready for production.")
        print("  Restart Claude Desktop to load the new server.")
    else:
        print(f"  {total - passed} tests failed. Check the errors above.")
    
    print("="*60)
    
    return passed == total


if __name__ == "__main__":
    # Run the tests
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
