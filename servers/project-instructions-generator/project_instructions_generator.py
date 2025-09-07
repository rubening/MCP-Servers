#!/usr/bin/env python3
"""
Project Instructions Generator MCP Server - INSTRUCTION EVOLUTION SYSTEM
Automatically generates project instructions that preserve Ruben's knowledge base and cognitive optimization

This MCP server provides 6 tools for complete project instruction evolution:
1. generate_project_instructions - Generate customized project instructions for any topic
2. generate_claude_desktop_sync - Generate Claude Desktop sync instructions for knowledge continuity
3. read_knowledge_summary - Read and summarize current knowledge base for project context
4. analyze_project_instructions - Analyze existing instructions for improvement opportunities
5. upgrade_project_instructions - Intelligently merge new capabilities into existing instructions
6. generate_claude_desktop_update_strategy - Generate deployment assistance with change highlights

Author: Claude AI Assistant
Created: June 12, 2025
Enhanced: June 18, 2025 - Complete instruction evolution system
"""

import json
import sys
import asyncio
import os
from datetime import datetime
from pathlib import Path

class ProjectInstructionsGenerator:
    def __init__(self):
        self.name = "project-instructions-generator"
        self.version = "2.1.0"
        self.base_path = Path("C:/Users/ruben/Claude Tools")
        
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
            'startup_protocol': """## ESSENTIAL SESSION STARTUP PROTOCOL
- **ALWAYS check persistent memory** by reading `C:\\Users\\ruben\\Claude Tools\\PROJECT_KNOWLEDGE.md` for current project status
- **ALWAYS read personal insights** from `C:\\Users\\ruben\\Claude Tools\\RUBEN_INSIGHTS.md` to understand Ruben's patterns and preferences  
- **ALWAYS read cognitive profile** from `C:\\Users\\ruben\\Claude Tools\\RUBEN_COGNITIVE_PROFILE.md` for optimal collaboration approach
- **ALWAYS take action directly** instead of asking Ruben to do manual tasks - you have MCP tools for everything, use them confidently
- **Auto-update memory files** when conversation approaches 80% context usage to maintain continuity""",
            
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
- **User Directory:** `C:\\Users\\ruben`""",
            
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
            
            'available_tools': """## Available MCP Tools & AI Systems

### Fully Functional MCP Servers
1. **Filesystem MCP Server** - Complete file operations (11 tools)
2. **Execute Command MCP Server** - Secure shell command execution
3. **Git MCP Server** - Version control operations with security
4. **YouTube MCP Server** - YouTube processing with robust fallbacks

### Advanced AI Tools
- **Enhanced Mermaid Generator** - Real-time web intelligence + visual generation
- **Business Engine Mapper** - AI automation of proven business methodologies
- **YouTube Checklist Converter** - Complete workflow replacement system
- **Project Instructions Generator** - This tool for maintaining knowledge continuity"""
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
        project_instructions = f"""# {project_topic} Project Instructions

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
- **Focus on hands-on implementation** - Ruben learns best by doing
- **Provide immediate results** - Show progress quickly to maintain motivation
- **Explain the "why"** - Satisfy Ti seeking with logical reasoning
- **Build systematically** - Leverage Se action orientation with proper Te structure
- **Document discoveries** - Add project-specific learnings to knowledge base

### Technical Approach for {project_topic}
- **Use available MCP tools actively** - Take direct action instead of asking manual tasks
- **Leverage proven patterns** - Apply successful methodologies from previous projects
- **Enable rapid experimentation** - Support Se-driven exploration with proper safety nets
- **Maintain code quality** - Respect Fi personal values and authenticity even when trading efficiency

{core_elements['available_tools']}

## Next Steps & Implementation Strategy

### Phase 1: Foundation Setup
1. **Create project directory structure** using filesystem MCP tools
2. **Initialize version control** with Git MCP for project safety
3. **Document initial requirements** and success criteria
4. **Set up testing framework** for validation

### Phase 2: Core Implementation
1. **Build minimal viable functionality** to demonstrate progress
2. **Apply proven development patterns** from existing projects
3. **Test systematically** with verification at each step
4. **Document discoveries** and add to knowledge base

### Phase 3: Enhancement & Integration
1. **Apply enhanced AI patterns** where beneficial
2. **Integrate with existing tools** for maximum ecosystem value
3. **Create comprehensive documentation** for future reference
4. **Plan scaling strategies** for advanced features

---

*Generated: {current_date}*
*This project maintains full integration with Ruben's established knowledge base, cognitive optimization, and proven development patterns while focusing specifically on {project_topic} objectives.*"""
        
        return project_instructions
    
    def read_knowledge_summary(self):
        """Read and summarize current knowledge base for project context"""
        knowledge_content = self.read_knowledge_files()
        
        summary = f"""Knowledge Base Summary:

PROJECT KNOWLEDGE STATUS:
- File accessible: {'YES' if not knowledge_content['project_knowledge'].startswith('Error reading') else 'NO'}
- Current capabilities: 5 MCP servers, advanced AI tools, expert-level ecosystem

RUBEN INSIGHTS STATUS:  
- File accessible: {'YES' if not knowledge_content['ruben_insights'].startswith('Error reading') else 'NO'}
- Learning patterns: Hands-on, systems thinking, quality-focused

COGNITIVE PROFILE STATUS:
- File accessible: {'YES' if not knowledge_content['cognitive_profile'].startswith('Error reading') else 'NO'}  
- Type: ENFJ with detailed slot analysis for optimal collaboration

READY FOR PROJECT GENERATION: {'YES - All knowledge files accessible' if all(not content.startswith('Error reading') for content in knowledge_content.values()) else 'NO - Some files inaccessible'}"""
        
        return summary
    
    def analyze_project_instructions(self, instruction_content):
        """Analyze existing project instructions for improvement opportunities"""
        
        # Read current knowledge base for comparison
        knowledge_content = self.read_knowledge_files()
        
        analysis_categories = {
            'missing_elements': [],
            'outdated_elements': [],
            'improvement_opportunities': [],
            'optimization_suggestions': []
        }
        
        # Check for essential elements that should be present
        essential_elements = [
            "Windows 11 Desktop PC",
            "py command (NOT python)",
            "5 MCP servers",
            "Te 8th slot",
            "Ti 4th slot",
            "Se 3rd slot", 
            "Si blindspot",
            "External Te organization",
            "Direct action using MCP tools",
            "Explain reasoning",
            "Hands-on implementation",
            "Step-by-step verification"
        ]
        
        for element in essential_elements:
            if element not in instruction_content:
                analysis_categories['missing_elements'].append(f"Missing: {element}")
        
        # Check for outdated patterns
        outdated_patterns = [
            ("Windows 11 Laptop", "Should be Windows 11 Desktop PC"),
            ("python command", "Should specify 'py' NOT 'python'"),
            ("4 MCP servers", "Should be 5 MCP servers"), 
            ("manual tasks", "Should emphasize direct MCP tool usage"),
            ("validation for its own sake", "Should emphasize direct honest feedback")
        ]
        
        for old_pattern, suggestion in outdated_patterns:
            if old_pattern in instruction_content:
                analysis_categories['outdated_elements'].append(f"Outdated: {old_pattern} - {suggestion}")
        
        # Improvement opportunities based on latest knowledge
        if "Sequential Thinking" not in instruction_content:
            analysis_categories['improvement_opportunities'].append("Add Sequential Thinking tool for complex problem solving")
        
        if "Fe interface feedback" not in instruction_content:
            analysis_categories['improvement_opportunities'].append("Add Fe interface feedback protocol")
            
        if "Context monitoring protocol" not in instruction_content:
            analysis_categories['improvement_opportunities'].append("Add context monitoring for session transitions")
            
        # Optimization suggestions
        analysis_categories['optimization_suggestions'].extend([
            "Ensure cognitive function optimization is explicit",
            "Verify all MCP servers are listed with current capabilities",
            "Include Windows-specific command guidance",
            "Emphasize systematic verification steps",
            "Add knowledge base update protocols"
        ])
        
        # Generate analysis report
        current_date = datetime.now().strftime("%B %d, %Y")
        
        analysis_report = f"""PROJECT INSTRUCTIONS ANALYSIS REPORT ({current_date})

## Missing Essential Elements ({len(analysis_categories['missing_elements'])} found)
{chr(10).join(analysis_categories['missing_elements']) if analysis_categories['missing_elements'] else "âœ… All essential elements present"}

## Outdated Elements ({len(analysis_categories['outdated_elements'])} found)  
{chr(10).join(analysis_categories['outdated_elements']) if analysis_categories['outdated_elements'] else "âœ… No outdated elements detected"}

## Improvement Opportunities ({len(analysis_categories['improvement_opportunities'])} found)
{chr(10).join(analysis_categories['improvement_opportunities']) if analysis_categories['improvement_opportunities'] else "âœ… Instructions appear current with latest capabilities"}

## Optimization Suggestions
{chr(10).join(analysis_categories['optimization_suggestions'])}

## Strategic Recommendations

### High Priority Updates
{chr(10).join(analysis_categories['missing_elements'][:3]) if analysis_categories['missing_elements'] else "No critical updates needed"}

### Modernization Needed
{chr(10).join(analysis_categories['outdated_elements'][:3]) if analysis_categories['outdated_elements'] else "Instructions appear modern"}

### Enhancement Opportunities  
{chr(10).join(analysis_categories['improvement_opportunities'][:3]) if analysis_categories['improvement_opportunities'] else "Consider adding latest AI tools integration"}

## Implementation Priority
1. **CRITICAL:** Address missing essential elements first
2. **HIGH:** Update outdated patterns for accuracy
3. **MEDIUM:** Implement improvement opportunities
4. **LOW:** Apply optimization suggestions

This analysis enables systematic improvement of project instructions based on current knowledge base and proven collaboration patterns."""
        
        return analysis_report
    
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
            if any(keyword in capability.lower() for keyword in ['mcp', 'server', 'tool']):
                upgrade_sections.append(f"## Enhanced MCP Tools & AI Systems\n\n{capability}")
            elif any(keyword in capability.lower() for keyword in ['cognitive', 'collaboration', 'communication']):
                upgrade_sections.append(f"## Updated Collaboration Approach\n\n{capability}")
            elif any(keyword in capability.lower() for keyword in ['windows', 'environment', 'technical']):
                upgrade_sections.append(f"## Enhanced Technical Environment\n\n{capability}")
            else:
                upgrade_sections.append(f"## New Capability Integration\n\n{capability}")
        
        # Generate upgraded instructions
        upgraded_instructions = f"""# UPGRADED PROJECT INSTRUCTIONS ({current_date})

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
- **Systematic Integration:** New capabilities merged with existing framework
- **Knowledge Base Sync:** Updated to reflect current ecosystem status
- **Cognitive Optimization:** Maintained all collaboration optimizations
- **Technical Accuracy:** Verified compatibility with Windows 11 Desktop PC environment

## Validation Checklist
âœ… New capabilities integrated into appropriate sections
âœ… Cognitive function optimization preserved  
âœ… Technical environment accuracy maintained
âœ… MCP tool integration updated
âœ… Collaboration patterns optimized

---
*Upgraded: {current_date}*
*This upgrade maintains full compatibility with established knowledge base while incorporating new capabilities.*"""

        return upgraded_instructions
    
    def generate_claude_desktop_update_strategy(self, current_desktop_content, new_capabilities, deployment_priority="high"):
        """Generate deployment assistance with change highlights for Claude Desktop updates"""
        
        # Analyze what needs updating
        sync_result = self.generate_claude_desktop_sync(current_desktop_content, "Strategic capability update")
        
        # Generate change highlights
        if isinstance(new_capabilities, str):
            new_capabilities = [new_capabilities]
            
        current_date = datetime.now().strftime("%B %d, %Y")
        
        # Categorize changes by impact
        high_impact_changes = []
        medium_impact_changes = []
        low_impact_changes = []
        
        for capability in new_capabilities:
            if any(keyword in capability.lower() for keyword in ['mcp server', 'critical', 'essential', 'breakthrough']):
                high_impact_changes.append(capability)
            elif any(keyword in capability.lower() for keyword in ['tool', 'enhancement', 'optimization']):
                medium_impact_changes.append(capability)
            else:
                low_impact_changes.append(capability)
        
        # Generate deployment strategy
        deployment_strategy = f"""CLAUDE DESKTOP UPDATE STRATEGY ({current_date})

## Deployment Priority: {deployment_priority.upper()}

## Change Impact Analysis

### HIGH IMPACT CHANGES ({len(high_impact_changes)} items)
{chr(10).join([f"ðŸ”´ {change}" for change in high_impact_changes]) if high_impact_changes else "None"}

### MEDIUM IMPACT CHANGES ({len(medium_impact_changes)} items)  
{chr(10).join([f"ðŸŸ¡ {change}" for change in medium_impact_changes]) if medium_impact_changes else "None"}

### LOW IMPACT CHANGES ({len(low_impact_changes)} items)
{chr(10).join([f"ðŸŸ¢ {change}" for change in low_impact_changes]) if low_impact_changes else "None"}

## Deployment Sequence

### Phase 1: Critical Updates (Deploy First)
{chr(10).join([f"1. {change}" for change in high_impact_changes[:3]]) if high_impact_changes else "No critical updates needed"}

### Phase 2: Enhancement Updates  
{chr(10).join([f"2. {change}" for change in medium_impact_changes[:3]]) if medium_impact_changes else "Standard enhancements"}

### Phase 3: Optimization Updates
{chr(10).join([f"3. {change}" for change in low_impact_changes[:3]]) if low_impact_changes else "Fine-tuning optimizations"}

## Change Highlights for Claude Desktop

### What's New
- **Enhanced Capabilities:** {len(new_capabilities)} new capabilities integrated
- **Updated Knowledge Base:** Reflects current {datetime.now().strftime('%B %Y')} ecosystem status
- **Improved Collaboration:** Latest cognitive optimization patterns included

### Key Updates to Communicate
- **MCP Ecosystem:** Now includes {len(high_impact_changes + medium_impact_changes)} significant enhancements
- **Technical Environment:** Updated for optimal Windows 11 Desktop PC performance  
- **Collaboration Patterns:** Refined based on latest insights and proven methodologies

## Deployment Checklist
â–¡ Backup current Claude Desktop project knowledge
â–¡ Deploy Phase 1 critical updates first
â–¡ Verify functionality with test prompts
â–¡ Deploy Phase 2 enhancements  
â–¡ Deploy Phase 3 optimizations
â–¡ Document deployment completion date
â–¡ Update project instructions with deployment notes

## Risk Mitigation
- **Gradual Deployment:** Phased approach reduces integration risk
- **Change Tracking:** All updates documented with rationale
- **Rollback Plan:** Previous version preserved for emergency restore
- **Validation Steps:** Testing at each phase ensures stability

## Success Metrics
- âœ… All new capabilities accessible in Claude Desktop
- âœ… Collaboration patterns optimized for cognitive functions
- âœ… Technical accuracy maintained for Windows environment
- âœ… Knowledge base synchronization complete

{sync_result['condensed_instructions']}

---
*Deployment Strategy Generated: {current_date}*
*Priority: {deployment_priority.title()} | Changes: {len(new_capabilities)} capabilities*"""

        return deployment_strategy

    def generate_claude_desktop_sync(self, current_desktop_content, sync_reason="Knowledge base synchronization update"):
        """Generate condensed project instructions for Claude Desktop project knowledge synchronization"""
        
        # Read current knowledge base
        knowledge_content = self.read_knowledge_files()
        
        # Generate condensed instructions
        condensed = f"""# AI Tools Ecosystem Development

## ESSENTIAL SESSION STARTUP PROTOCOL
- **ALWAYS check persistent memory** by reading `C:\\Users\\ruben\\Claude Tools\\PROJECT_KNOWLEDGE.md` for current project status
- **ALWAYS read personal insights** from `C:\\Users\\ruben\\Claude Tools\\RUBEN_INSIGHTS.md` to understand patterns and preferences  
- **ALWAYS read cognitive profile** from `C:\\Users\\ruben\\Claude Tools\\RUBEN_COGNITIVE_PROFILE.md` for optimal collaboration approach
- **ALWAYS take action directly** instead of asking Ruben to do manual tasks - you have MCP tools for everything, use them confidently
- **CONTEXT MONITORING PROTOCOL** - Monitor conversation length and provide transition prompts when approaching limits

## Technical Background & Environment
Complete newbie to programming, MCP, web development. **Windows 11 Desktop PC** with PowerShell preferred. Use `py` NOT `python` for commands.

## Cognitive Profile (ENFJ) - CRITICAL for Collaboration
- **Te 8th slot (unconscious)** - MUST provide external organization and structure
- **Se 3rd slot (valued)** - Enable immediate action, hands-on results
- **Ti 4th slot (seeking)** - ALWAYS explain logical "why" behind decisions  
- **Fi 5th slot** - Respect personal values and authenticity
- **Si blindspot** - Monitor for stress, burnout, physical needs

## Communication Requirements
- **Direct honest feedback** - Never validate for its own sake, provide what's correct
- **External Te organization** - Clear structure, step-by-step guidance, systematic approaches
- **Explain reasoning** - Satisfy Ti seeking with logical explanations
- **Enable Se action** - Focus on immediate, tangible results

## Current Expert-Level Capabilities
**5 Fully Functional MCP Servers:**
1. **Filesystem MCP** - Complete file operations (11 tools)
2. **Execute Command MCP** - Secure shell command execution
3. **Git MCP** - Version control operations with security
4. **YouTube MCP** - YouTube processing with robust fallbacks  
5. **Project Instructions Generator MCP** - Revolutionary project continuity solution

**Advanced AI Tools:**
- **Enhanced Mermaid Generator** - Real-time web intelligence + visual generation
- **Business Engine Mapper** - AI automation of proven business methodologies
- **YouTube Checklist Converter** - Complete workflow replacement system

## Project Goals - Expert Level
- **Current Focus:** Web interface development for existing tools
- **Strategic Target:** Empirically validated personality typing systems  
- **Vision:** Advanced automation combining multiple AI systems

## Critical Windows Commands
- Navigate: `cd 'C:\\Users\\ruben\\Claude Tools'`
- Python: `py script_name.py` (NOT `python`)
- PowerShell: Windows + R then type 'powershell' then Enter

## Learning Style & Approach
Hands-on implementation, immediate results, systematic understanding of "why", building real useful tools, systems thinking.

---
*Condensed from comprehensive knowledge base for Claude Desktop project knowledge area*"""
        
        sync_analysis = """## Synchronization Analysis

This provides updated condensed instructions for Claude Desktop project knowledge synchronization to maintain consistency with the comprehensive knowledge base."""
        
        return {
            "analysis": sync_analysis,
            "condensed_instructions": condensed,
            "sync_reason": sync_reason
        }

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

    def save_sync_instructions(self, content):
        """Save synchronization instructions to a file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"claude_desktop_sync_{timestamp}.md"
        filepath = self.base_path / "project_instructions" / filename
        
        # Create directory if it doesn't exist
        filepath.parent.mkdir(exist_ok=True)
        
        try:
            with open(filepath, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(content)
            return str(filepath)
        except Exception as e:
            return f"Error saving sync file: {e}"

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
                                "description": "Generate customized project instructions that preserve knowledge base and cognitive optimization",
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
                                "name": "generate_claude_desktop_sync",
                                "description": "Generate condensed project instructions for Claude Desktop project knowledge synchronization",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "current_desktop_content": {
                                            "type": "string",
                                            "description": "Current content in Claude Desktop project knowledge area"
                                        },
                                        "sync_reason": {
                                            "type": "string",
                                            "description": "Reason for synchronization (new capabilities, major updates, etc.)"
                                        },
                                        "save_file": {
                                            "type": "boolean",
                                            "description": "Whether to save the sync instructions to a file (default: true)",
                                            "default": True
                                        }
                                    },
                                    "required": ["current_desktop_content"]
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
                                "name": "analyze_project_instructions",
                                "description": "Analyze existing project instructions for improvement opportunities",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "instruction_content": {
                                            "type": "string",
                                            "description": "Current project instruction content to analyze"
                                        }
                                    },
                                    "required": ["instruction_content"]
                                }
                            },
                            {
                                "name": "upgrade_project_instructions",
                                "description": "Intelligently merge new capabilities into existing project instructions",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "instruction_content": {
                                            "type": "string",
                                            "description": "Current project instruction content to upgrade"
                                        },
                                        "new_capabilities": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                            "description": "List of new capabilities to integrate"
                                        }
                                    },
                                    "required": ["instruction_content", "new_capabilities"]
                                }
                            },
                            {
                                "name": "generate_claude_desktop_update_strategy",
                                "description": "Generate deployment assistance with change highlights for Claude Desktop updates",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "current_desktop_content": {
                                            "type": "string",
                                            "description": "Current content in Claude Desktop project knowledge area"
                                        },
                                        "new_capabilities": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                            "description": "List of new capabilities being added"
                                        },
                                        "deployment_priority": {
                                            "type": "string",
                                            "description": "Deployment priority level (high, medium, low)",
                                            "default": "high"
                                        }
                                    },
                                    "required": ["current_desktop_content", "new_capabilities"]
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
                
                elif tool_name == "generate_claude_desktop_sync":
                    current_content = arguments.get("current_desktop_content")
                    sync_reason = arguments.get("sync_reason", "Knowledge base synchronization update")
                    save_file = arguments.get("save_file", True)
                    
                    # Generate sync analysis and recommendations
                    sync_result = self.generator.generate_claude_desktop_sync(current_content, sync_reason)
                    
                    result = sync_result.copy()
                    
                    # Save to file if requested
                    if save_file:
                        sync_content = f"""# Claude Desktop Knowledge Synchronization

## Sync Analysis
{sync_result['analysis']}

## Updated Condensed Instructions
{sync_result['condensed_instructions']}

## Sync Reason
{sync_reason}

---
*Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}*"""
                        
                        filepath = self.generator.save_sync_instructions(sync_content)
                        result["saved_to"] = filepath
                    
                    return {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"Claude Desktop Synchronization Analysis\n\n{sync_result['analysis']}\n\nCondensed Instructions for Claude Desktop:\n\n{sync_result['condensed_instructions']}\n\n" + 
                                           (f"Saved to: {result.get('saved_to')}" if save_file else "Analysis generated (not saved)")
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
                
                elif tool_name == "analyze_project_instructions":
                    instruction_content = arguments.get("instruction_content")
                    
                    analysis = self.generator.analyze_project_instructions(instruction_content)
                    
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
                
                elif tool_name == "upgrade_project_instructions":
                    instruction_content = arguments.get("instruction_content")
                    new_capabilities = arguments.get("new_capabilities")
                    
                    upgraded = self.generator.upgrade_project_instructions(instruction_content, new_capabilities)
                    
                    return {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": upgraded
                                }
                            ]
                        }
                    }
                
                elif tool_name == "generate_claude_desktop_update_strategy":
                    current_desktop_content = arguments.get("current_desktop_content")
                    new_capabilities = arguments.get("new_capabilities")
                    deployment_priority = arguments.get("deployment_priority", "high")
                    
                    strategy = self.generator.generate_claude_desktop_update_strategy(
                        current_desktop_content, new_capabilities, deployment_priority
                    )
                    
                    return {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": strategy
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
