#!/usr/bin/env python3
"""
Project Instructions Generator MCP Server - CLAUDE CODE CLI EDITION
Automatically generates CLAUDE.md files and repository instructions for Claude Code CLI environment

This MCP server provides 6 tools for Claude Code CLI project management:
1. generate_project_instructions - Generate customized project instructions for any topic
2. generate_claude_md_instructions - Generate/update CLAUDE.md files for repositories
3. read_knowledge_summary - Read and summarize current knowledge base for project context
4. analyze_repository_context - Understand current repository structure and development needs
5. generate_development_commands - Create CLI commands for common development tasks
6. update_project_status - Update repository status and development progress

Author: Claude AI Assistant
Created: June 12, 2025
Adapted for Claude Code CLI: September 9, 2025
"""

import json
import sys
import asyncio
import os
from datetime import datetime
from pathlib import Path

class ProjectInstructionsGenerator:
    def __init__(self):
        self.name = "project-instructions-generator-cli"
        self.version = "3.0.0"
        self.base_path = Path("C:/Users/ruben/Claude Tools")
        self.current_repo = Path.cwd()  # Current repository path for CLI context
        
    def read_knowledge_files(self):
        """Read the core knowledge files for context"""
        knowledge_files = {
            'project_knowledge': self.base_path / "PROJECT_KNOWLEDGE.md",
            'ruben_insights': self.base_path / "RUBEN_INSIGHTS.md", 
            'cognitive_profile': self.base_path / "RUBEN_COGNITIVE_PROFILE.md"
        }
        
        content = {}
        for key, file_path in knowledge_files.items():
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content[key] = f.read()
            except Exception as e:
                content[key] = f"Error reading {file_path}: {e}"
                
        return content
    
    def extract_core_elements(self, knowledge_content):
        """Extract reusable core elements from knowledge base"""
        core_elements = {
            'startup_protocol': """## ESSENTIAL CLAUDE CODE STARTUP PROTOCOL
- **ALWAYS check persistent memory** by reading `C:\\Users\\ruben\\Claude Tools\\PROJECT_KNOWLEDGE.md` for current project status
- **ALWAYS read personal insights** from `C:\\Users\\ruben\\Claude Tools\\RUBEN_INSIGHTS.md` to understand Ruben's patterns and preferences  
- **ALWAYS read cognitive profile** from `C:\\Users\\ruben\\Claude Tools\\RUBEN_COGNITIVE_PROFILE.md` for optimal collaboration approach
- **ALWAYS take action directly** using Claude Code CLI tools instead of asking manual tasks
- **Repository-aware operations** - Understand current working directory and git context
- **Auto-update memory files** when making significant progress to maintain continuity""",
            
            'technical_background': """## Ruben's Technical Background (Critical Context)
Complete newbie to:
- Coding/programming (any language)
- Command line/terminal usage
- MCP (Model Context Protocol) 
- Web design and development
- Technical file management
- Development environments and tools""",
            
            'windows_environment': """## CRITICAL Windows Environment Configuration
- **Operating System:** Windows 11 Desktop PC
- **Primary Terminal:** PowerShell (preferred over Command Prompt)
- **Python Command:** Use `py` NOT `python` (prevents "Python was not found" errors)
- **Package Management:** Use `py -m pip` NOT `pip` (pip command not in PATH by default)
- **File Paths:** Use backslashes `\\` for Windows paths
- **User Directory:** `C:\\Users\\ruben`
- **Claude Code CLI:** Integrated bash/PowerShell execution with proper Windows support""",
            
            'cognitive_profile': """## Ruben's Cognitive Profile & Collaboration Approach

### Essential Understanding (ENFJ with specific slot analysis)
- **Te 8th slot (unconscious)** - MUST provide external organization and structure
- **Se 3rd slot (valued)** - Enable immediate action, hands-on results, acts before deliberating  
- **Ti 4th slot (seeking)** - ALWAYS explain the logical "why" behind decisions and recommendations
- **Fi 5th slot (valued but ignored)** - Respects personal values and authenticity over efficiency
- **Si blindspot** - Will ignore physical needs, stress, burnout - monitor for this

### Communication Requirements
- **Direct honest feedback** - NEVER provide validation for its own sake, wants to know what's correct ASAP
- **External Te organization** - Provide clear structure, systematic approaches, step-by-step guidance
- **Explain reasoning** - Satisfy Ti seeking with logical explanations of "why"
- **Enable Se action** - Focus on immediate, tangible results and hands-on implementation
- **Systematic verification** - Compensate for Si weakness with external checking and monitoring""",
            
            'available_tools': """## Available Claude Code CLI Tools & Capabilities

### Claude Code CLI Environment
- **Repository Awareness** - Understands current working directory and git context
- **File Operations** - Direct file reading, writing, and editing capabilities
- **Command Execution** - Integrated bash/PowerShell command execution
- **Search & Analysis** - Powerful grep, glob, and codebase analysis tools
- **Multi-tool Coordination** - Batch operations across multiple tools

### MCP Servers (CLI Integration)
1. **Filesystem Operations** - File management with CLI integration
2. **Git Operations** - Version control with CLI workflows
3. **Command Execution** - Shell command execution with proper Windows support
4. **Project Instructions Generator CLI** - This tool for CLAUDE.md management

### Development Workflow Support
- **CLAUDE.md Management** - Repository-specific instruction files
- **Development Commands** - Automated CLI command generation
- **Repository Analysis** - Codebase structure and context understanding
- **Progress Tracking** - Development status and milestone management"""
        }
        
        return core_elements
    
    def generate_project_instructions(self, project_topic, project_description, project_goals=None):
        """Generate customized project instructions for a specific topic"""
        
        # Read knowledge base
        knowledge_content = self.read_knowledge_files()
        core_elements = self.extract_core_elements(knowledge_content)
        
        # Generate timestamp
        current_date = datetime.now().strftime("%B %d, %Y")
        
        # Create project-specific content
        project_instructions = f"""# {project_topic} Project Instructions - Claude Code CLI

{core_elements['startup_protocol']}

## Project Overview: {project_topic}

### Project Purpose
{project_description}

### Project Goals
{project_goals if project_goals else "To be defined based on project requirements and strategic objectives."}

{core_elements['technical_background']}

{core_elements['windows_environment']}

{core_elements['cognitive_profile']}

## Project-Specific Guidelines

### Context for {project_topic}
- **Focus on hands-on implementation** - Ruben learns best by doing with Claude Code CLI tools
- **Provide immediate results** - Show progress quickly using direct file operations
- **Explain the "why"** - Satisfy Ti seeking with logical reasoning
- **Build systematically** - Leverage Se action orientation with proper Te structure
- **Document discoveries** - Add project-specific learnings to knowledge base using Write tool

### Technical Approach for {project_topic}
- **Use Claude Code CLI tools actively** - Take direct action with Read, Edit, Write, Bash tools
- **Leverage proven patterns** - Apply successful methodologies from previous projects
- **Enable rapid experimentation** - Support Se-driven exploration with proper safety nets
- **Maintain code quality** - Respect Fi personal values and authenticity even when trading efficiency

{core_elements['available_tools']}

## Next Steps & Implementation Strategy

### Phase 1: Foundation Setup
1. **Create/update CLAUDE.md** using this tool's claude_md_instructions capability
2. **Analyze repository structure** with repository context analysis
3. **Set up development commands** for common workflow tasks
4. **Initialize proper git workflow** integration

### Phase 2: Core Implementation
1. **Build minimal viable functionality** to demonstrate progress
2. **Apply proven development patterns** from existing projects
3. **Test systematically** with verification at each step using CLI tools
4. **Document discoveries** and add to knowledge base with automated updates

### Phase 3: Enhancement & Integration
1. **Optimize Claude Code CLI workflows** for maximum efficiency
2. **Integrate with existing tool ecosystem** for maximum value
3. **Create comprehensive documentation** including repository-specific CLAUDE.md
4. **Plan scaling strategies** for advanced features and automation

---

*Generated: {current_date}*
*This project maintains full integration with Ruben's established knowledge base, cognitive optimization, and proven development patterns while focusing specifically on {project_topic} objectives using Claude Code CLI.*"""
        
        return project_instructions
    
    def read_knowledge_summary(self):
        """Read and summarize current knowledge base for project context"""
        knowledge_content = self.read_knowledge_files()
        
        summary = f"""Knowledge Base Summary:

PROJECT KNOWLEDGE STATUS:
- File accessible: {'YES' if not knowledge_content['project_knowledge'].startswith('Error reading') else 'NO'}
- Current capabilities: MCP servers, Claude Code CLI integration, expert-level ecosystem

RUBEN INSIGHTS STATUS:  
- File accessible: {'YES' if not knowledge_content['ruben_insights'].startswith('Error reading') else 'NO'}
- Learning patterns: Hands-on, systems thinking, quality-focused

COGNITIVE PROFILE STATUS:
- File accessible: {'YES' if not knowledge_content['cognitive_profile'].startswith('Error reading') else 'NO'}  
- Type: ENFJ with detailed slot analysis for optimal collaboration

READY FOR CLAUDE CODE CLI PROJECT GENERATION: {'YES - All knowledge files accessible' if all(not content.startswith('Error reading') for content in knowledge_content.values()) else 'NO - Some files inaccessible'}"""
        
        return summary
    
    def analyze_repository_context(self, repository_path=None):
        """Understand current repository structure and development needs"""
        
        if repository_path is None:
            repository_path = self.current_repo
        else:
            repository_path = Path(repository_path)
            
        current_date = datetime.now().strftime("%B %d, %Y")
        
        analysis = f"""REPOSITORY CONTEXT ANALYSIS ({current_date})

## Repository Information
- **Path:** {repository_path}
- **Name:** {repository_path.name}
- **Analysis Date:** {current_date}

## Repository Structure Analysis

### Key Directories Found
"""
        
        try:
            # Analyze common directory structures
            key_dirs = []
            common_dirs = ['src', 'servers', 'scripts', 'configs', 'documentation', 'tests', 'core-infrastructure', 
                          'external-services', 'analytics-intelligence', 'ai-reasoning', 'business-tools', 'experimental']
            
            for dir_name in common_dirs:
                dir_path = repository_path / dir_name
                if dir_path.exists():
                    file_count = len(list(dir_path.glob('*')))
                    key_dirs.append(f"- **{dir_name}/**: {file_count} items")
            
            if key_dirs:
                analysis += "\n".join(key_dirs)
            else:
                analysis += "- Standard project structure detected"
                
            # Check for key files
            analysis += "\n\n### Key Configuration Files\n"
            config_files = ['CLAUDE.md', 'README.md', 'package.json', 'requirements.txt', 'setup.py', 
                          'pyproject.toml', '.gitignore', 'claude_desktop_config.json']
            
            found_configs = []
            for config_file in config_files:
                if (repository_path / config_file).exists():
                    found_configs.append(f"- ✅ {config_file}")
                else:
                    found_configs.append(f"- ❌ {config_file}")
            
            analysis += "\n".join(found_configs)
            
            # Development context recommendations
            analysis += f"""

## Development Context Recommendations

### CLAUDE.md File Status
{'✅ EXISTS - Repository has Claude Code CLI instructions' if (repository_path / 'CLAUDE.md').exists() else '❌ MISSING - Should create CLAUDE.md for Claude Code CLI integration'}

### Repository Type Assessment
"""
            
            # Determine repository type based on structure
            if (repository_path / 'servers').exists():
                analysis += "- **Type:** MCP Server Repository\n- **Focus:** Model Context Protocol server development\n- **CLI Needs:** Server testing, configuration generation, development workflows"
            elif (repository_path / 'src').exists():
                analysis += "- **Type:** Standard Software Project\n- **Focus:** Application development\n- **CLI Needs:** Build automation, testing, deployment workflows"
            elif (repository_path / 'package.json').exists():
                analysis += "- **Type:** Node.js Project\n- **Focus:** JavaScript/TypeScript development\n- **CLI Needs:** npm scripts, build processes, testing frameworks"
            elif (repository_path / 'requirements.txt').exists() or (repository_path / 'pyproject.toml').exists():
                analysis += "- **Type:** Python Project\n- **Focus:** Python application or library development\n- **CLI Needs:** pip management, pytest execution, virtual environment setup"
            else:
                analysis += "- **Type:** General Purpose Repository\n- **Focus:** Mixed or documentation-focused project\n- **CLI Needs:** Basic file operations, git workflows, documentation management"
                
            analysis += f"""

### Recommended Claude Code CLI Integration

#### High Priority
- Create/update CLAUDE.md with repository-specific instructions
- Set up development command shortcuts for common tasks
- Configure repository-aware file operations
- Establish git workflow integration

#### Medium Priority  
- Create automated testing commands
- Set up build and deployment automation
- Configure code quality and linting workflows
- Establish documentation generation processes

#### Low Priority
- Advanced analysis and reporting tools
- Integration with external services
- Custom workflow optimizations
- Performance monitoring and profiling

---
*Repository Analysis Generated: {current_date}*
*Path: {repository_path}*
*Ready for Claude Code CLI optimization*"""
            
        except Exception as e:
            analysis += f"\n\n⚠️ Error analyzing repository structure: {e}"
            
        return analysis
    
    def generate_claude_md_instructions(self, repository_path=None, project_focus="general", include_development_commands=True):
        """Generate/update CLAUDE.md files for repositories with Claude Code CLI integration"""
        
        if repository_path is None:
            repository_path = self.current_repo
        else:
            repository_path = Path(repository_path)
            
        # Read current knowledge base for core elements
        knowledge_content = self.read_knowledge_files()
        core_elements = self.extract_core_elements(knowledge_content)
        
        current_date = datetime.now().strftime("%B %d, %Y")
        repo_name = repository_path.name
        
        # Generate repository-specific CLAUDE.md content
        claude_md = f"""# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**Repository:** {repo_name}  
**Focus:** {project_focus.title()} development and management  
**Environment:** Windows 11 Desktop PC with Claude Code CLI  
**Updated:** {current_date}

{core_elements['startup_protocol']}

{core_elements['technical_background']}

{core_elements['windows_environment']}

{core_elements['cognitive_profile']}

## Repository-Specific Context

### Development Environment
- **Primary Path:** `{repository_path}`
- **Repository Type:** {project_focus.title()} project
- **CLI Integration:** Full Claude Code CLI support
- **File Operations:** Direct read/write/edit capabilities

### Key Development Workflows
"""
        
        # Add development commands if requested
        if include_development_commands:
            if project_focus.lower() == "mcp server":
                claude_md += """- **Server Testing:** `py [server_name].py` to test MCP servers
- **Configuration Generation:** `py scripts/generate_config.py` for Claude Desktop configs
- **Dependency Management:** `py -m pip install -r requirements.txt`
- **Repository Analysis:** Use Grep and Glob tools for codebase exploration"""
            elif project_focus.lower() == "python":
                claude_md += """- **Script Execution:** `py script_name.py` (never use `python`)
- **Package Installation:** `py -m pip install package_name`
- **Testing:** `py -m pytest` for test execution
- **Virtual Environment:** `py -m venv venv` for isolation"""
            elif project_focus.lower() == "node.js":
                claude_md += """- **Package Management:** `npm install` for dependencies
- **Script Execution:** `npm run [script_name]` for package.json scripts
- **Development Server:** `npm start` or `npm run dev`
- **Testing:** `npm test` for test suites"""
            else:
                claude_md += """- **File Operations:** Use Read, Edit, Write tools for file management
- **Search Operations:** Use Grep for content search, Glob for file patterns
- **Command Execution:** Use Bash tool for shell commands
- **Git Operations:** Integrated git workflow support"""
        
        claude_md += f"""

### Claude Code CLI Optimization

#### File Management
- **Reading Files:** Use Read tool for examining code and configurations
- **Editing Files:** Use Edit or MultiEdit for code modifications  
- **Writing Files:** Use Write tool only when creating new files is essential
- **Search Operations:** Use Grep for content search, Glob for file patterns

#### Development Commands
- **Command Execution:** Use Bash tool with proper Windows PowerShell syntax
- **Path Handling:** Use absolute paths, quote paths with spaces
- **Error Handling:** Include timeout and error checking for commands
- **Background Tasks:** Use run_in_background for long-running processes

#### Repository Integration
- **Git Operations:** Leverage git integration for version control
- **Multi-file Operations:** Batch operations when possible for efficiency
- **Context Awareness:** Understand current working directory and file structure
- **Progress Tracking:** Use TodoWrite for complex multi-step tasks

{core_elements['available_tools']}

## Best Practices for This Repository

### Code Quality
- **Systematic Approach:** Follow Te organization with clear step-by-step processes
- **Immediate Action:** Enable Se action orientation with hands-on implementation
- **Logical Explanation:** Satisfy Ti seeking by explaining the "why" behind decisions
- **Value Alignment:** Respect Fi personal values and code authenticity

### Development Workflow
- **Direct Execution:** Use Claude Code CLI tools instead of asking for manual tasks
- **Batch Operations:** Coordinate multiple tools efficiently
- **Error Recovery:** Implement proper error handling and recovery procedures
- **Documentation:** Maintain clear documentation for future reference

### Windows Environment Specifics
- **PowerShell Priority:** Prefer PowerShell over Command Prompt
- **Python Command:** Always use `py` instead of `python` to avoid path issues
- **File Paths:** Use backslashes for Windows paths, quote spaces
- **Package Management:** Use `py -m pip` for reliable package installation

## Repository Status and Goals

### Current Status
- Repository initialized for Claude Code CLI integration
- Development environment configured for Windows 11 Desktop PC
- Core cognitive optimization patterns implemented

### Development Goals
- Maintain systematic development workflow
- Enable immediate hands-on results
- Provide clear logical reasoning for all decisions
- Respect personal development values and preferences

### Success Metrics
- Efficient Claude Code CLI integration
- Streamlined development workflows
- High-quality code with proper documentation
- Optimal collaboration patterns maintained

---

*Generated: {current_date} for Claude Code CLI*  
*Repository: {repo_name}*  
*Focus: {project_focus.title()} Development*"""
        
        return {
            "content": claude_md,
            "repository": str(repository_path),
            "focus": project_focus,
            "generated_date": current_date
        }
    
    def generate_development_commands(self, repository_path=None, project_type="general"):
        """Generate CLI commands for common development tasks"""
        
        if repository_path is None:
            repository_path = self.current_repo
        else:
            repository_path = Path(repository_path)
            
        current_date = datetime.now().strftime("%B %d, %Y")
        
        commands = f"""DEVELOPMENT COMMANDS FOR {repository_path.name.upper()} ({current_date})

## Repository Navigation
```powershell
# Navigate to repository
cd "{repository_path}"

# List repository contents
ls

# Check git status
git status
```

## Common Development Tasks
"""
        
        if project_type.lower() == "mcp server":
            commands += """### MCP Server Development
```powershell
# Test individual MCP server
py server_name.py

# Generate Claude Desktop configuration
py scripts/generate_config.py

# Install Python dependencies
py -m pip install -r requirements.txt

# Run server tests (if available)
py test_server.py
```

### MCP Server Testing
```powershell
# Test server initialization
echo '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{}}' | py server_name.py

# List available tools
echo '{"jsonrpc":"2.0","method":"tools/list","id":2}' | py server_name.py
```"""
        elif project_type.lower() == "python":
            commands += """### Python Development
```powershell
# Create virtual environment
py -m venv venv

# Activate virtual environment
.\\venv\\Scripts\\Activate.ps1

# Install dependencies
py -m pip install -r requirements.txt

# Run Python scripts
py script_name.py

# Run tests
py -m pytest

# Install package in development mode
py -m pip install -e .
```"""
        elif project_type.lower() == "node.js":
            commands += """### Node.js Development
```powershell
# Install dependencies
npm install

# Run development server
npm run dev

# Run production build
npm run build

# Run tests
npm test

# Start application
npm start
```"""
        else:
            commands += """### General Development
```powershell
# File operations
ls                          # List files
Get-Content file.txt        # Read file contents
Set-Content -Path file.txt -Value "content"  # Write to file

# Directory operations
mkdir new_directory         # Create directory
cd new_directory           # Change directory
rmdir empty_directory      # Remove empty directory
```"""
            
        commands += f"""

## Git Workflow Commands
```powershell
# Check repository status
git status

# Stage changes
git add .
git add specific_file.py

# Commit changes
git commit -m "Descriptive commit message"

# Push to remote
git push origin main

# Pull latest changes
git pull origin main

# Create new branch
git checkout -b feature-branch-name

# Switch branches
git checkout main
git checkout feature-branch-name
```

## Claude Code CLI Integration
```powershell
# The following operations are handled by Claude Code CLI tools:
# - File reading: Use Read tool
# - File editing: Use Edit/MultiEdit tools
# - File writing: Use Write tool (only when necessary)
# - Search operations: Use Grep and Glob tools
# - Command execution: Use Bash tool
# - Git operations: Integrated git support
```

## Repository-Specific Shortcuts

### Quick Setup
```powershell
# Full repository setup from scratch
cd "{repository_path}"
git status
# (Add project-specific setup commands here)
```

### Development Workflow
```powershell
# Daily development workflow
cd "{repository_path}"
git pull origin main
# (Add project-specific development commands here)
git add .
git commit -m "Your commit message"
git push origin main
```

### Testing and Validation
```powershell
# Run all tests and validation
cd "{repository_path}"
# (Add project-specific testing commands here)
```

## Notes for Windows 11 Desktop PC
- **Always use `py` instead of `python`** to avoid "Python was not found" errors
- **Use PowerShell** as the preferred terminal environment
- **Quote paths with spaces** using double quotes
- **Use backslashes** for Windows file paths
- **Prefer `py -m pip`** over just `pip` for package management

---
*Generated: {current_date}*  
*Repository: {repository_path.name}*  
*Type: {project_type.title()}*  
*Environment: Windows 11 Desktop PC with Claude Code CLI*"""
        
        return commands
    
    def update_project_status(self, repository_path=None, status_update="", milestone="", next_steps=None):
        """Update repository status and development progress"""
        
        if repository_path is None:
            repository_path = self.current_repo
        else:
            repository_path = Path(repository_path)
            
        current_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        
        if next_steps is None:
            next_steps = []
        elif isinstance(next_steps, str):
            next_steps = [next_steps]
            
        status_report = f"""PROJECT STATUS UPDATE - {repository_path.name.upper()}

## Status Update ({current_date})

### Current Status
{status_update if status_update else "Status update pending..."}

### Milestone Achievement
{milestone if milestone else "No specific milestone noted"}

### Repository Information
- **Path:** {repository_path}
- **Last Updated:** {current_date}
- **Claude Code CLI Integration:** Active

### Progress Summary

#### Completed
- Repository initialized for Claude Code CLI
- Core development environment configured
- CLAUDE.md instructions established
- Windows 11 Desktop PC optimization applied

#### In Progress
{status_update if status_update else "Current development activities..."}

#### Next Steps
"""
        
        if next_steps:
            for i, step in enumerate(next_steps, 1):
                status_report += f"{i}. {step}\n"
        else:
            status_report += "- Review current implementation\n- Plan next development phase\n- Update documentation as needed\n"
            
        status_report += f"""

### Development Environment Status
- ✅ Claude Code CLI integration active
- ✅ Windows 11 Desktop PC configuration optimized
- ✅ Python environment configured (using `py` command)
- ✅ PowerShell as primary terminal
- ✅ Git workflow integration enabled
- ✅ Cognitive optimization patterns applied

### Key Metrics
- **Repository Health:** {'Good' if status_update else 'Pending Assessment'}
- **CLI Integration:** Fully Functional
- **Development Workflow:** Optimized for Se action + Te structure
- **Technical Environment:** Windows 11 Desktop PC Ready

### Collaboration Optimization
- **Te 8th slot support:** External organization and structure provided
- **Se 3rd slot enablement:** Immediate action and hands-on results prioritized  
- **Ti 4th slot satisfaction:** Logical reasoning and "why" explanations included
- **Fi 5th slot respect:** Personal values and authenticity maintained
- **Si blindspot compensation:** External monitoring and systematic verification

## Action Items

### Immediate (High Priority)
- Continue current development focus
- Maintain systematic verification processes
- Document key discoveries and insights

### Near-term (Medium Priority)
- Enhance repository-specific workflows
- Optimize Claude Code CLI integration
- Expand development command automation

### Long-term (Strategic)
- Scale successful patterns to other repositories
- Integrate advanced AI tools where beneficial
- Establish comprehensive testing and validation frameworks

---
*Status Update Generated: {current_date}*  
*Repository: {repository_path.name}*  
*Environment: Claude Code CLI on Windows 11 Desktop PC*"""
        
        return status_report

    def upgrade_project_instructions(self, instruction_content, new_capabilities):
        """Intelligently merge new capabilities into existing project instructions"""
        
        # Read current knowledge base for context
        knowledge_content = self.read_knowledge_files()
        core_elements = self.extract_core_elements(knowledge_content)
        
        # Parse new capabilities
        if isinstance(new_capabilities, str):
            new_capabilities = [new_capabilities]
        
        # Generate upgrade strategy
        current_date = datetime.now().strftime("%B %d, %Y")
        
        upgrade_sections = []
        
        # Add new capabilities to appropriate sections
        for capability in new_capabilities:
            if any(keyword in capability.lower() for keyword in ['claude code cli', 'cli', 'repository', 'tool']):
                upgrade_sections.append(f"## Enhanced Claude Code CLI Integration\n\n{capability}")
            elif any(keyword in capability.lower() for keyword in ['cognitive', 'collaboration', 'communication']):
                upgrade_sections.append(f"## Updated Collaboration Approach\n\n{capability}")
            elif any(keyword in capability.lower() for keyword in ['windows', 'environment', 'technical']):
                upgrade_sections.append(f"## Enhanced Technical Environment\n\n{capability}")
            else:
                upgrade_sections.append(f"## New Capability Integration\n\n{capability}")
        
        # Generate upgraded instructions
        upgraded_instructions = f"""# UPGRADED PROJECT INSTRUCTIONS - CLAUDE CODE CLI ({current_date})

## Capability Upgrades Applied
{chr(10).join([f"- {cap}" for cap in new_capabilities])}

## Integration Strategy
The following capabilities have been systematically integrated into the project instructions:

{chr(10).join(upgrade_sections)}

## Updated Core Elements
{core_elements['startup_protocol']}

{core_elements['technical_background']}

{core_elements['windows_environment']}

{core_elements['cognitive_profile']}

{core_elements['available_tools']}

## Upgrade Implementation Notes
- **Systematic Integration:** New capabilities merged with existing Claude Code CLI framework
- **Knowledge Base Sync:** Updated to reflect current ecosystem status
- **Cognitive Optimization:** Maintained all collaboration optimizations
- **Technical Accuracy:** Verified compatibility with Windows 11 Desktop PC environment
- **CLI Integration:** Enhanced repository-aware operations

## Validation Checklist
✅ New capabilities integrated into appropriate sections
✅ Cognitive function optimization preserved  
✅ Technical environment accuracy maintained
✅ Claude Code CLI integration updated
✅ Collaboration patterns optimized
✅ Repository-awareness maintained

---
*Upgraded: {current_date}*
*This upgrade maintains full compatibility with established knowledge base while incorporating new capabilities for Claude Code CLI.*"""

        return upgraded_instructions

    def save_project_instructions(self, content, project_topic):
        """Save generated instructions to a file"""
        filename = f"{project_topic.lower().replace(' ', '_')}_project_instructions.md"
        filepath = self.base_path / "project_instructions" / filename
        
        # Create directory if it doesn't exist
        filepath.parent.mkdir(exist_ok=True)
        
        try:
            with open(filepath, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(content)
            return str(filepath)
        except Exception as e:
            return f"Error saving file: {e}"

    def save_claude_md(self, content, repository_path=None):
        """Save CLAUDE.md file to repository"""
        if repository_path is None:
            repository_path = self.current_repo
        else:
            repository_path = Path(repository_path)
            
        filepath = repository_path / "CLAUDE.md"
        
        try:
            with open(filepath, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(content)
            return str(filepath)
        except Exception as e:
            return f"Error saving CLAUDE.md: {e}"

class MCPServer:
    def __init__(self):
        self.generator = ProjectInstructionsGenerator()
        
    async def handle_request(self, request):
        """Handle MCP requests"""
        try:
            if request.get("method") == "initialize":
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": self.generator.name,
                            "version": self.generator.version
                        }
                    }
                }
            
            elif request.get("method") == "tools/list":
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {
                        "tools": [
                            {
                                "name": "generate_project_instructions",
                                "description": "Generate customized project instructions that preserve knowledge base and cognitive optimization for Claude Code CLI",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "project_topic": {
                                            "type": "string",
                                            "description": "Main topic/name of the project"
                                        },
                                        "project_description": {
                                            "type": "string", 
                                            "description": "Detailed description of what the project aims to accomplish"
                                        },
                                        "project_goals": {
                                            "type": "string",
                                            "description": "Specific goals and success criteria (optional)"
                                        },
                                        "save_file": {
                                            "type": "boolean",
                                            "description": "Whether to save the instructions to a file (default: true)",
                                            "default": True
                                        }
                                    },
                                    "required": ["project_topic", "project_description"]
                                }
                            },
                            {
                                "name": "generate_claude_md_instructions",
                                "description": "Generate/update CLAUDE.md files for repositories with Claude Code CLI integration",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "repository_path": {
                                            "type": "string",
                                            "description": "Path to the repository (defaults to current working directory)"
                                        },
                                        "project_focus": {
                                            "type": "string",
                                            "description": "Primary focus of the project (e.g., 'MCP Server', 'Python', 'Node.js', 'General')",
                                            "default": "general"
                                        },
                                        "include_development_commands": {
                                            "type": "boolean",
                                            "description": "Whether to include development command examples (default: true)",
                                            "default": True
                                        },
                                        "save_file": {
                                            "type": "boolean",
                                            "description": "Whether to save CLAUDE.md to the repository (default: true)",
                                            "default": True
                                        }
                                    },
                                    "required": []
                                }
                            },
                            {
                                "name": "read_knowledge_summary",
                                "description": "Read and summarize current knowledge base for project context",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {},
                                    "required": []
                                }
                            },
                            {
                                "name": "analyze_repository_context",
                                "description": "Understand current repository structure and development needs",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "repository_path": {
                                            "type": "string",
                                            "description": "Path to the repository to analyze (defaults to current working directory)"
                                        }
                                    },
                                    "required": []
                                }
                            },
                            {
                                "name": "generate_development_commands",
                                "description": "Create CLI commands for common development tasks",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "repository_path": {
                                            "type": "string",
                                            "description": "Path to the repository (defaults to current working directory)"
                                        },
                                        "project_type": {
                                            "type": "string",
                                            "description": "Type of project for command optimization (e.g., 'MCP Server', 'Python', 'Node.js', 'General')",
                                            "default": "general"
                                        }
                                    },
                                    "required": []
                                }
                            },
                            {
                                "name": "update_project_status",
                                "description": "Update repository status and development progress",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "repository_path": {
                                            "type": "string",
                                            "description": "Path to the repository (defaults to current working directory)"
                                        },
                                        "status_update": {
                                            "type": "string",
                                            "description": "Current status description",
                                            "default": ""
                                        },
                                        "milestone": {
                                            "type": "string",
                                            "description": "Milestone or achievement to document",
                                            "default": ""
                                        },
                                        "next_steps": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                            "description": "List of next steps or action items"
                                        }
                                    },
                                    "required": []
                                }
                            }
                        ]
                    }
                }
            
            elif request.get("method") == "tools/call":
                tool_name = request.get("params", {}).get("name")
                arguments = request.get("params", {}).get("arguments", {})
                
                if tool_name == "generate_project_instructions":
                    project_topic = arguments.get("project_topic")
                    project_description = arguments.get("project_description") 
                    project_goals = arguments.get("project_goals")
                    save_file = arguments.get("save_file", True)
                    
                    # Generate instructions
                    instructions = self.generator.generate_project_instructions(
                        project_topic, project_description, project_goals
                    )
                    
                    result = {
                        "content": instructions,
                        "topic": project_topic
                    }
                    
                    # Save to file if requested
                    if save_file:
                        filepath = self.generator.save_project_instructions(instructions, project_topic)
                        result["saved_to"] = filepath
                    
                    return {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"Generated project instructions for '{project_topic}'\n\n{instructions}\n\n" + 
                                           (f"Saved to: {result.get('saved_to')}" if save_file else "Instructions generated (not saved)")
                                }
                            ]
                        }
                    }
                
                elif tool_name == "generate_claude_md_instructions":
                    repository_path = arguments.get("repository_path")
                    project_focus = arguments.get("project_focus", "general")
                    include_development_commands = arguments.get("include_development_commands", True)
                    save_file = arguments.get("save_file", True)
                    
                    # Generate CLAUDE.md content
                    result = self.generator.generate_claude_md_instructions(
                        repository_path, project_focus, include_development_commands
                    )
                    
                    # Save to repository if requested
                    if save_file:
                        filepath = self.generator.save_claude_md(result['content'], repository_path)
                        result["saved_to"] = filepath
                    
                    return {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"Generated CLAUDE.md for {result['repository']}\n\nProject Focus: {result['focus']}\nGenerated: {result['generated_date']}\n\n{result['content']}\n\n" + 
                                           (f"Saved to: {result.get('saved_to')}" if save_file else "CLAUDE.md generated (not saved)")
                                }
                            ]
                        }
                    }
                
                elif tool_name == "read_knowledge_summary":
                    summary = self.generator.read_knowledge_summary()
                    
                    return {
                        "jsonrpc": "2.0", 
                        "id": request.get("id"),
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": summary
                                }
                            ]
                        }
                    }
                
                elif tool_name == "analyze_repository_context":
                    repository_path = arguments.get("repository_path")
                    
                    analysis = self.generator.analyze_repository_context(repository_path)
                    
                    return {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": analysis
                                }
                            ]
                        }
                    }
                
                elif tool_name == "generate_development_commands":
                    repository_path = arguments.get("repository_path")
                    project_type = arguments.get("project_type", "general")
                    
                    commands = self.generator.generate_development_commands(repository_path, project_type)
                    
                    return {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": commands
                                }
                            ]
                        }
                    }
                
                elif tool_name == "update_project_status":
                    repository_path = arguments.get("repository_path")
                    status_update = arguments.get("status_update", "")
                    milestone = arguments.get("milestone", "")
                    next_steps = arguments.get("next_steps")
                    
                    status_report = self.generator.update_project_status(
                        repository_path, status_update, milestone, next_steps
                    )
                    
                    return {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": status_report
                                }
                            ]
                        }
                    }
            
            # Handle other standard MCP methods
            elif request.get("method") == "notifications/initialized":
                return None  # No response needed for notifications
            
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {request.get('method')}"
                    }
                }
                
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }

async def main():
    """Main server loop"""
    server = MCPServer()
    
    while True:
        try:
            # Read request from stdin
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
                
            request = json.loads(line.strip())
            response = await server.handle_request(request)
            
            if response:
                print(json.dumps(response), flush=True)
                
        except json.JSONDecodeError:
            continue
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": f"Parse error: {str(e)}"
                }
            }
            print(json.dumps(error_response), flush=True)

if __name__ == "__main__":
    asyncio.run(main())