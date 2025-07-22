# CROSS-PLATFORM MCP SYNCHRONIZATION GUIDE
*Windows â†” Mac M4 deployment and maintenance strategy*

## OVERVIEW
This guide establishes the synchronization strategy between Ruben's Windows 11 development environment and Mac M4 production deployment, ensuring seamless MCP server management across both platforms.

## PLATFORM ARCHITECTURE

### **Windows 11 (Development Hub)**
- **Role**: Primary development, testing, configuration
- **Location**: `C:\Users\ruben\OneDrive\MCP_Servers`
- **Claude Desktop Config**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Python**: `py` command (not `python`)
- **Package Manager**: `py -m pip`
- **Version Control**: Git repository with OneDrive sync

### **Mac M4 (Production Target)**
- **Role**: Production deployment, daily usage
- **Location**: `~/OneDrive/MCP_Servers` (synced from Windows)
- **Claude Desktop Config**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Python**: Standard `python3` command
- **Package Manager**: `pip3` or `python3 -m pip`
- **Architecture**: ARM64 compatibility required

## SYNCHRONIZATION STRATEGY

### **Method 1: OneDrive Automatic Sync (Recommended)**
**Advantages:**
- Automatic file synchronization
- Version history preservation
- No manual intervention required
- Cross-platform file access

**Implementation:**
1. **Windows**: Keep development in `C:\Users\ruben\OneDrive\MCP_Servers`
2. **Mac**: Access via `~/OneDrive/MCP_Servers`
3. **Git**: Repository remains synced across platforms
4. **Configs**: Platform-specific configurations maintained separately

### **Method 2: Git Repository Sync (Backup Method)**
**Advantages:**
- Version control integrity
- Manual control over sync timing
- Professional development workflow

**Implementation:**
```bash
# Windows (PowerShell)
cd "C:\Users\ruben\OneDrive\MCP_Servers"
git add .
git commit -m "Update from Windows development"
git push

# Mac (Terminal)
cd ~/OneDrive/MCP_Servers
git pull
```

## CONFIGURATION MANAGEMENT

### **Windows Configuration Template**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "py",
      "args": ["C:\\Users\\ruben\\OneDrive\\MCP_Servers\\working-servers-backup\\core-infrastructure\\filesystem_mcp.py"]
    },
    "git": {
      "command": "py", 
      "args": ["C:\\Users\\ruben\\OneDrive\\MCP_Servers\\working-servers-backup\\core-infrastructure\\git_mcp.py"]
    },
    "deepseek": {
      "command": "py",
      "args": ["C:\\Users\\ruben\\OneDrive\\MCP_Servers\\working-servers\\ai-services\\deepseek_mcp.py"]
    }
  }
}
```

### **Mac Configuration Template**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "python3",
      "args": ["/Users/ruben/OneDrive/MCP_Servers/working-servers-backup/core-infrastructure/filesystem_mcp.py"]
    },
    "git": {
      "command": "python3",
      "args": ["/Users/ruben/OneDrive/MCP_Servers/working-servers-backup/core-infrastructure/git_mcp.py"]
    },
    "deepseek": {
      "command": "python3", 
      "args": ["/Users/ruben/OneDrive/MCP_Servers/working-servers/ai-services/deepseek_mcp.py"]
    }
  }
}
```

## PLATFORM-SPECIFIC CONSIDERATIONS

### **Windows Specific**
- **Python Command**: Always use `py` not `python`
- **Pip Command**: Use `py -m pip install package`
- **Path Format**: Backslashes `C:\Users\ruben\...`
- **PowerShell**: Preferred terminal environment
- **File Permissions**: Usually not an issue

### **Mac M4 Specific**
- **Python Command**: Use `python3` or `python`
- **Pip Command**: Use `pip3 install package` or `python3 -m pip`
- **Path Format**: Forward slashes `/Users/ruben/...`
- **Terminal**: Bash or Zsh
- **ARM64**: Ensure packages are M4 compatible
- **Permissions**: May need `chmod +x` for execution

## DEPENDENCY MANAGEMENT

### **Shared Requirements Approach**
Create platform-agnostic requirements files:

**File**: `requirements.txt` (Cross-platform base)
```
mcp>=0.1.0
asyncio>=3.4.3
typing>=3.7.4
```

**File**: `requirements-windows.txt` (Windows-specific)
```
-r requirements.txt
windows-curses>=2.3.0
```

**File**: `requirements-mac.txt` (Mac-specific)  
```
-r requirements.txt
# Mac-specific packages if needed
```

### **Installation Commands**

**Windows:**
```powershell
cd "C:\Users\ruben\OneDrive\MCP_Servers"
py -m pip install -r requirements-windows.txt
```

**Mac:**
```bash
cd ~/OneDrive/MCP_Servers
python3 -m pip install -r requirements-mac.txt
```

## AUTOMATED SYNC SCRIPTS

### **Windows Sync Script** (`sync-to-mac.ps1`)
```powershell
# Windows PowerShell script for preparing Mac deployment
param([string]$ServerName = "all")

Write-Host "Preparing MCP servers for Mac deployment..." -ForegroundColor Green

# Update git repository
Set-Location "C:\Users\ruben\OneDrive\MCP_Servers"
git add .
git commit -m "Windows development update - $(Get-Date)"
git push

# Generate Mac configuration
python generate_mac_config.py

Write-Host "Ready for Mac sync via OneDrive" -ForegroundColor Green
```

### **Mac Setup Script** (`setup-mac.sh`)
```bash
#!/bin/bash
# Mac setup script for MCP servers

echo "Setting up MCP servers on Mac M4..."

# Navigate to synced directory
cd ~/OneDrive/MCP_Servers

# Pull latest from git
git pull

# Install dependencies
python3 -m pip install -r requirements-mac.txt

# Set execute permissions
find . -name "*.py" -exec chmod +x {} \;

# Copy Mac-specific configuration
cp configs/claude_desktop_config_MAC.json ~/Library/Application\ Support/Claude/claude_desktop_config.json

echo "Mac M4 setup complete!"
```

## TESTING STRATEGY

### **Development Testing (Windows)**
1. **Local Testing**: Test all servers on Windows first
2. **Configuration Validation**: Verify config file syntax
3. **Dependency Check**: Ensure all packages install correctly
4. **Git Sync**: Commit working changes

### **Production Testing (Mac)**
1. **Sync Verification**: Confirm files synchronized correctly
2. **Dependency Installation**: Install Mac-specific requirements
3. **Configuration Update**: Apply Mac-specific config
4. **Functionality Test**: Verify each server works on Mac
5. **Performance Check**: Ensure M4 optimization

## DEPLOYMENT WORKFLOW

### **Phase 1: Windows Development**
1. Develop and test MCP servers on Windows
2. Update configurations and documentation
3. Commit changes to Git repository
4. Generate Mac-specific configurations

### **Phase 2: Synchronization**
1. **Automatic**: OneDrive syncs files to Mac
2. **Manual**: Git pull on Mac if needed
3. **Verification**: Check file integrity

### **Phase 3: Mac Deployment**
1. Run Mac setup script
2. Install Mac-specific dependencies
3. Update Claude Desktop configuration
4. Test server functionality
5. Validate performance

## TROUBLESHOOTING

### **Common Sync Issues**

**Problem**: Python command not found on Mac
**Solution**: 
```bash
# Install Python 3 via Homebrew
brew install python3
# Or use system Python
which python3
```

**Problem**: Permission denied on Mac
**Solution**:
```bash
chmod +x ~/OneDrive/MCP_Servers/working-servers/**/*.py
```

**Problem**: OneDrive sync conflicts
**Solution**:
1. Check OneDrive sync status
2. Resolve conflicts manually
3. Use Git as backup sync method

### **Configuration Issues**

**Problem**: Wrong file paths in config
**Solution**: Use path conversion utility
```python
# Path converter utility
import os
windows_path = "C:\\Users\\ruben\\OneDrive\\MCP_Servers\\..."
mac_path = windows_path.replace("C:\\Users\\ruben", "/Users/ruben").replace("\\", "/")
```

**Problem**: Package compatibility on M4
**Solution**: Check ARM64 compatibility
```bash
python3 -m pip install --only-binary=:all: package_name
```

## MAINTENANCE SCHEDULE

### **Weekly Tasks**
- [ ] Sync development changes from Windows to Mac
- [ ] Test critical servers on both platforms
- [ ] Update requirements files if needed
- [ ] Backup configurations

### **Monthly Tasks**
- [ ] Update Python packages on both platforms
- [ ] Review and optimize configurations
- [ ] Performance benchmarking
- [ ] Documentation updates

### **Quarterly Tasks**
- [ ] Major version updates
- [ ] Security audit of configurations
- [ ] Workflow optimization review
- [ ] Backup verification

## SUCCESS METRICS

### **Sync Reliability**
- **Target**: 99% successful automatic syncs
- **Measure**: OneDrive sync success rate
- **Backup**: Git push/pull success rate

### **Platform Compatibility**
- **Target**: 100% server functionality on both platforms
- **Measure**: Server response success rate
- **Test**: Weekly cross-platform validation

### **Deployment Speed**
- **Target**: < 5 minutes Windows to Mac deployment
- **Measure**: Time from Windows commit to Mac functionality
- **Optimize**: Automated script efficiency

---

## QUICK REFERENCE

### **Windows Commands**
```powershell
# Navigate to MCP servers
cd "C:\Users\ruben\OneDrive\MCP_Servers"

# Install packages
py -m pip install package_name

# Git operations
git add . && git commit -m "Update" && git push
```

### **Mac Commands**
```bash
# Navigate to MCP servers
cd ~/OneDrive/MCP_Servers

# Install packages  
python3 -m pip install package_name

# Git operations
git pull && python3 -m pip install -r requirements-mac.txt
```

### **Configuration Locations**
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`

---
*Last Updated: July 22, 2025*
*Cross-Platform Strategy: Seamless development to production workflow*