import os
import json
from string import Template

def generate_mcp_config():
    """Generate OneDrive-based MCP config for testing"""
    
    print("🔄 Generating MCP config from template...")
    
    # Paths (these replace the {{}} placeholders)
    onedrive_path = "C:\\Users\\ruben\\OneDrive"
    local_secure_path = "C:\\Users\\ruben\\Claude Tools"
    
    print(f"📁 OneDrive path: {onedrive_path}")
    print(f"🔐 Local secure path: {local_secure_path}")
    
    # Load template
    template_path = f"{onedrive_path}\\MCP_Servers\\configs\\mcp_template.json"
    print(f"📖 Reading template: {template_path}")
    
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    # Replace all {{ONEDRIVE_PATH}} with real path
    # Replace all {{LOCAL_SECURE_PATH}} with real path
    template = Template(template_content)
    config_content = template.substitute(
        ONEDRIVE_PATH=onedrive_path,
        LOCAL_SECURE_PATH=local_secure_path
    )
    
    # Save test config (don't overwrite active config yet!)
    test_config_path = f"{onedrive_path}\\MCP_Servers\\configs\\claude_desktop_config_TEST.json"
    with open(test_config_path, 'w') as f:
        f.write(config_content)
    
    print(f"✅ Generated TEST config: {test_config_path}")
    print("🔍 This file now has REAL paths (no more {{}} placeholders)")
    print("🎯 When ready to test, copy to Claude Desktop config location")
    print("💡 Your current Claude setup is completely untouched!")

if __name__ == "__main__":
    generate_mcp_config()
