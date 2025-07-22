#!/usr/bin/env python3
"""
Basic test to check server import and initialization
"""

import sys
import os

print("Starting basic server test...")

# Add the server directory to path
sys.path.append('C:\\Users\\ruben\\OneDrive\\Documents\\mcp_servers\\mcp-project-optimizer')

try:
    print("Attempting to import server...")
    from server import ProjectKnowledgeOptimizerMCP
    print("âœ“ Server imported successfully!")
    
    print("Attempting to initialize server...")
    server = ProjectKnowledgeOptimizerMCP()
    print("âœ“ Server initialized successfully!")
    
    print("BASIC TEST PASSED!")
    
except Exception as e:
    print(f"ERROR: {str(e)}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    print("Full traceback:")
    traceback.print_exc()

print("Test completed.")
