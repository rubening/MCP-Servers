# Scripts and Commands Reference
**Complete catalog of all tools, scripts, and commands in your AI Tools Ecosystem**  
*Created for Si PoLR support - Easy reference for all your assets*

## Quick Navigation
- [Essential Commands](#essential-commands)
- [MCP Servers](#mcp-servers)
- [AI Tools](#ai-tools)
- [Research Tools](#research-tools)
- [Git & Version Control](#git--version-control)
- [Utility Scripts](#utility-scripts)
- [File Locations](#file-locations)
- [Common Workflows](#common-workflows)

---

## Essential Commands

### Quick Commit (NEW!)
**Purpose:** One-command commit for both repositories  
**Location:** `C:\Users\ruben\Claude Tools\quick-commit.ps1`  
**Usage:**
```powershell
.\quick-commit.ps1
.\quick-commit.ps1 -Message "Add new feature"
.\quick-commit.ps1 -Message "Fix issue" -Verbose
```

### Navigate to Main Project
```powershell
cd 'C:\Users\ruben\Claude Tools'
```

### Check Git Status
```powershell
# Via MCP (in Claude)
git_status for both repos

# Direct command
git status
```

---

## MCP Servers
*All configured in Claude Desktop and ready to use*

### 1. Filesystem MCP
**Purpose:** Complete file operations  
**Location:** `C:\Users\ruben\Claude Tools\mcp-servers\filesystem_mcp.py`  
**Capabilities:**
- `list_directory` - Browse folders
- `read_file` - Read individual files  
- `write_file` - Create/overwrite files
- `edit_file` - Modify specific parts
- `create_directory` - Make new folders
- `directory_tree` - Show folder structure
- `move_file` - Move/rename files
- `search_files` - Find by name/content
- `get_file_info` - Detailed file info

### 2. Execute Command MCP
**Purpose:** Secure shell command execution  
**Location:** `C:\Users\ruben\Claude Tools\mcp-servers\execute_command_mcp.py`  
**Capabilities:**
- `execute_command` - Run shell commands safely
- `get_system_info` - System information
- `list_dangerous_commands` - Security info
- **Log:** `C:\Users\ruben\Claude Tools\logs\execute_command_mcp.log`

### 3. Git MCP  
**Purpose:** Version control operations  
**Location:** `C:\Users\ruben\Claude Tools\mcp-servers\git_mcp.py`  
**Capabilities:**
- `git_status` - Repository status
- `git_add` - Stage files
- `git_commit` - Create commits
- `git_push` - Push to remote
- `git_pull` - Pull from remote
- `git_branch` - Branch operations
- `git_log` - Commit history
- **Log:** `C:\Users\ruben\Claude Tools\logs\git_mcp.log`

### 4. YouTube MCP
**Purpose:** YouTube transcript extraction and processing  
**Location:** `C:\Users\ruben\Claude Tools\mcp-servers\youtube_mcp.py`  
**Capabilities:**
- `youtube_to_checklist` - URL to actionable checklist
- `youtube_transcript` - Extract transcript only
- `youtube_debug` - Troubleshoot extraction
- **Log:** `C:\Users\ruben\Claude Tools\logs\youtube_mcp.log`

### 5. Project Instructions Generator MCP
**Purpose:** Automated project setup with knowledge preservation  
**Location:** `C:\Users\ruben\Claude Tools\mcp-servers\project_instructions_generator.py`  
**Capabilities:**
- `generate_project_instructions` - Create custom project instructions
- `read_knowledge_summary` - Verify knowledge base
- **Breakthrough:** Maintains continuity across Claude sessions

---

## Research Tools
*Personality typing and cognitive function research framework*

### Cognitive Function Tests Document
**Purpose:** Comprehensive theoretical framework and behavioral testing methodology  
**Location:** `C:\Users\ruben\Claude Tools\COGNITIVE_FUNCTION_TESTS.md`

**Core Frameworks:**
- **Slot Function Definitions** - 1st: who you are, 2nd: how you are (tool), 3rd: for what purpose, 4th: who you are not
- **2nd-3rd Slot Engine Theory** - The "little engine" driving each type
- **Terminology Development** - Custom system avoiding confusion between existing approaches
- **Testing Categories** - Positive, Negative, Seeking, PoLR behavioral indicators

**Documented Test Results:**
- **Ruben (ENFJ) Confirmed Tests** - 5 function tests with behavioral evidence
- **Ni (2nd Slot)** - Strong positive: Single encapsulation capability
- **Ne (6th Slot)** - Counter-valued: Preference against option generation
- **Se (3rd Slot)** - Satisfaction source: Impact and action orientation
- **Ti (4th Slot)** - Seeking: Logical explanation requests
- **Si (7th Slot)** - PoLR: External compensation needs

**Usage for Test Addition:**
```
"Add this to cognitive function tests: [behavior observed] indicates [function] [slot position] because [reasoning]"
```

**Research Applications:**
- Cross-type engine validation
- Behavioral prediction testing  
- Assessment tool development
- Empirical validation methodology

---

## AI Tools
*Enhanced AI-powered automation systems*

### Enhanced Mermaid Generator
**Purpose:** Create diagrams with real-time web intelligence  
**Location:** `C:\Users\ruben\Claude Tools\projects\ai-tools\mermaid-generator\`

**Files:**
- `mermaid_generator.py` - Manual diagram creation
- `ai_prompt_generator.py` - Natural language to diagrams  
- `enhanced_ai_generator.py` - **WEB-ENHANCED with real-time data**

**Usage:**
```powershell
cd 'C:\Users\ruben\Claude Tools\projects\ai-tools\mermaid-generator'
python enhanced_ai_generator.py
```

**Output:** `diagrams/` folder with `.mmd` files viewable at https://mermaid.live/

### Business Engine Mapper
**Purpose:** AI automation of Ryan Deiss $200M business methodology  
**Location:** `C:\Users\ruben\Claude Tools\projects\ai-tools\business-engine-mapper\`

**Files:**
- `business_engine_mapper.py` - Core system
- `enhanced_business_engine_mapper.py` - Web-enhanced version
- `demo.py` - Interactive demonstration

**Revolutionary Features:**
- Instant business process mapping
- Market intelligence integration
- Professional deliverables in seconds

### YouTube Checklist Converter
**Purpose:** Complete replacement for n8n workflow  
**Location:** `C:\Users\ruben\Claude Tools\projects\ai-tools\youtube-checklister\`

**Files:**
- `youtube_checklister.py` - Main converter
- `debug_transcript.py` - Troubleshooting tool
- `demo.py` - Demonstration script

**Advantages over n8n:**
- Zero external APIs
- No monthly costs  
- Better AI processing
- Complete local control

---

## Git & Version Control

### Repository Structure
```
Claude Tools/ (Main repo)
â”œâ”€â”€ projects/ai-tools/ (Submodule)
â”œâ”€â”€ logs/ (MCP operation logs)
â”œâ”€â”€ PROJECT_KNOWLEDGE.md (Persistent memory)
â””â”€â”€ quick-commit.ps1 (NEW!)
```

### Quick Commit Script (NEW!)
**Purpose:** One command for complete repository sync  
**Location:** `C:\Users\ruben\Claude Tools\quick-commit.ps1`

**What it does:**
1. Commits changes in ai-tools submodule
2. Updates main repository 
3. Syncs all logs
4. Shows final status

**Usage:**
```powershell
# Basic commit
.\quick-commit.ps1

# Custom message
.\quick-commit.ps1 -Message "Add new MCP server"

# Verbose output
.\quick-commit.ps1 -Message "Fix generator bug" -Verbose
```

### Manual Git Workflow
If you need manual control:
```powershell
# Check status
git status

# In submodule first
cd 'C:\Users\ruben\Claude Tools\projects\ai-tools'
git add .
git commit -m "Your message"

# Then main repo  
cd 'C:\Users\ruben\Claude Tools'
git add .
git commit -m "Update submodule and sync"
```

---

## Utility Scripts

### Process Video Scripts
**Purpose:** YouTube video processing workflows  
**Location:** `C:\Users\ruben\Claude Tools\`

**Files:**
- `process_video.py` - Basic processing
- `robust_process_video.py` - Enhanced error handling
- `process_ryan_deiss_video.py` - Business-specific processing

### Adaptive Demo Systems
**Purpose:** Demonstration of adaptive AI frameworks  
**Location:** `C:\Users\ruben\Claude Tools\`

**Files:**
- `adaptive_demo.py` - Basic adaptive system demo
- `adaptive_system_demo.py` - Advanced adaptive framework

---

## File Locations

### Core Knowledge Files
```
C:\Users\ruben\Claude Tools\
â”œâ”€â”€ PROJECT_KNOWLEDGE.md (Main memory)
â”œâ”€â”€ RUBEN_COGNITIVE_PROFILE.md (Collaboration optimization)
â”œâ”€â”€ RUBEN_INSIGHTS.md (Learning patterns)
â”œâ”€â”€ COGNITIVE_FUNCTION_TESTS.md (Personality typing research framework)
â”œâ”€â”€ SCRIPTS_AND_COMMANDS_REFERENCE.md (This document - complete tool catalog)
â””â”€â”€ quick-commit.ps1 (One-command repository sync)
```

### MCP Servers
```
C:\Users\ruben\Claude Tools\mcp-servers\
â”œâ”€â”€ filesystem_mcp.py
â”œâ”€â”€ execute_command_mcp.py  
â”œâ”€â”€ git_mcp.py
â”œâ”€â”€ youtube_mcp.py
â””â”€â”€ project_instructions_generator.py
```

### AI Tools Collection
```
C:\Users\ruben\Claude Tools\projects\ai-tools\
â”œâ”€â”€ mermaid-generator/
â”œâ”€â”€ business-engine-mapper/
â”œâ”€â”€ youtube-checklister/
â”œâ”€â”€ project-instructions-generator/
â”œâ”€â”€ execute-command-mcp/
â”œâ”€â”€ filesystem-mcp/
â””â”€â”€ git-mcp/
```

### Generated Content
```
# Diagrams
C:\Users\ruben\Claude Tools\projects\ai-tools\mermaid-generator\diagrams\

# Business outputs  
C:\Users\ruben\Claude Tools\projects\ai-tools\business-engine-mapper\engines\

# YouTube outputs
C:\Users\ruben\Claude Tools\projects\ai-tools\youtube-checklister\outputs\

# Project instructions
C:\Users\ruben\Claude Tools\project_instructions\
```

---

## Common Workflows

### Starting a New Session
1. **Claude reads your memory automatically** (no action needed)
2. **Check recent changes:** `git status` via MCP
3. **If needed, commit:** `.\quick-commit.ps1`

### Adding New Features
1. **Develop in appropriate directory**
2. **Test the feature**
3. **Commit with quick script:** `.\quick-commit.ps1 -Message "Add [feature name]"`

### Creating Diagrams
1. **Use Claude MCP tools** for instant generation
2. **Or manually:** Navigate to mermaid-generator and run Python scripts
3. **View at:** https://mermaid.live/

### Processing YouTube Videos
1. **Via MCP:** Use `youtube_to_checklist` tool in Claude
2. **Manually:** Run scripts in youtube-checklister directory
3. **Output:** Check outputs folder for results

### Business Analysis
1. **Via Claude:** Request business engine mapping
2. **Manually:** Run business-engine-mapper scripts
3. **Get:** Complete business process diagrams and analysis

---

## Windows-Specific Commands

### Navigation
```powershell
# Change directory (with spaces)
cd 'C:\Users\ruben\Claude Tools'

# List files
dir
ls

# Current location
pwd
```

### Python Execution
```powershell
# Use python launcher (preferred)
py script_name.py

# If py doesn't work
python script_name.py

# With full path (last resort)
C:\Users\ruben\AppData\Local\Programs\Python\Python313\python.exe script_name.py
```

### PowerShell Scripts
```powershell
# Run script
.\script-name.ps1

# With parameters
.\script-name.ps1 -Parameter "value"

# Get help
Get-Help .\script-name.ps1
```

---

## Troubleshooting

### Python Not Found
- Use `py` instead of `python`
- Check if Python is in PATH
- Use full path as last resort

### Git Command Issues
- Use MCP tools in Claude instead
- Check if Git is installed and in PATH

### MCP Server Issues  
- Check Claude Desktop configuration
- Look at log files in `logs/` directory
- Restart Claude Desktop if needed

### File Permission Issues
- Run PowerShell as Administrator
- Check file/directory permissions
- Ensure you're in correct directory

---

## Quick Reference Card

### Most Used Commands
```powershell
# Quick commit everything
.\quick-commit.ps1

# Navigate to main project
cd 'C:\Users\ruben\Claude Tools'

# Check status  
git status

# Run Python script
py script_name.py

# List files
dir
```

### Most Used Claude MCP Commands
- `git_status` - Check repository status
- `youtube_to_checklist` - Process YouTube videos
- `read_file` - Read any file
- `write_file` - Create/edit files
- `directory_tree` - See folder structure

---

*This reference document provides complete access to all your AI tools and automation capabilities. Bookmark this for easy Si detail support!*

**Last Updated:** June 12, 2025  
**Total Tools:** 5 MCP Servers + 10+ AI Tools + 1 Quick Commit Script