print("Hello from Python!")
print("Testing basic functionality...")

import sys
print(f"Python version: {sys.version}")
print(f"Current working directory: {sys.path[0] if sys.path else 'unknown'}")

import os
print(f"Files in current directory: {os.listdir('.')}")

# Test if we can find our src directory
if os.path.exists('src'):
    print("âœ“ Found src directory")
    print(f"  Files in src: {os.listdir('src')}")
else:
    print("âœ— No src directory found")

# Test if sample file exists
if os.path.exists('sample_project_knowledge.md'):
    print("âœ“ Found sample file")
    with open('sample_project_knowledge.md', 'r') as f:
        content = f.read()
        print(f"  Sample file has {len(content.split())} words")
else:
    print("âœ— No sample file found")

print("Basic test completed!")
