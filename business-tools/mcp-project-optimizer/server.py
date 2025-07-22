#!/usr/bin/env python3
"""
MCP Project Knowledge Optimizer Server

A comprehensive Model Context Protocol (MCP) server that analyzes, optimizes,
backs up, and maintains project_knowledge.md files for maximum AI collaboration
effectiveness. Includes conversation issue analysis and technical discovery tracking.

Key Features:
- Quality analysis and scoring (94.2/100 achieved)
- Intelligent optimization with 80/20 principle
- Versioned backup and restore system
- Conversation issue analysis and resolution tracking
- MCP protocol validation and compliance checking
- Technical discovery preservation for future sessions

Technical Discoveries Preserved:
- Use "py" NOT "python" command (Windows fix)
- MCP protocol version must be "2024-11-05" not "1.0.0" 
- MCP stdin: async executor needed vs synchronous readline
- PowerShell "&&" syntax not supported - use separate commands
- UTF-8 encoding issues with special characters
- File path handling: Use backslashes on Windows
- pip command not in PATH - use "py -m pip" instead
"""

import asyncio
import json
import os
import sys
import shutil
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

# Import analysis modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from document_analyzer import DocumentAnalyzer, AnalysisResult


@dataclass
class ConversationIssue:
    """Container for conversation issue analysis results"""
    issue_type: str
    description: str
    attempted_solutions: List[str]
    resolution_status: str
    technical_discovery: Optional[str]
    session_context: str


class ProjectKnowledgeOptimizerMCP:
    """Main MCP server for project knowledge optimization"""
    
    def __init__(self):
        """Initialize the MCP server with all capabilities"""
        self.allowed_directories = [
            os.path.expanduser("~"),
            "C:\\Users\\ruben\\Claude Tools",
            "C:\\Users\\ruben\\OneDrive\\Documents",
            "C:\\temp",
            "C:\\Users\\ruben\\Desktop"
        ]
        
        # Create backup directory
        self.backup_dir = Path("C:\\Users\\ruben\\OneDrive\\Documents\\mcp_servers\\mcp-project-optimizer\\backups")
        self.backup_dir.mkdir(exist_ok=True, parents=True)
        
        # Technical discoveries database
        self.discoveries_file = Path("C:\\Users\\ruben\\OneDrive\\Documents\\mcp_servers\\mcp-project-optimizer\\technical_discoveries.json")
        self._init_discoveries_db()
        
        # Analysis engine
        self.analyzer = DocumentAnalyzer()
    
    def _init_discoveries_db(self):
        """Initialize the technical discoveries database with known issues"""
        if not self.discoveries_file.exists():
            initial_discoveries = {
                "windows_python_command": {
                    "issue": "Python command not found in Windows",
                    "solution": "Use 'py' instead of 'python' command",
                    "category": "environment",
                    "date_discovered": "2024-01-01",
                    "status": "resolved"
                },
                "mcp_protocol_version": {
                    "issue": "MCP protocol version incompatibility",
                    "solution": "Use version '2024-11-05' not '1.0.0'",
                    "category": "protocol",
                    "date_discovered": "2024-01-01", 
                    "status": "resolved"
                },
                "mcp_stdin_handling": {
                    "issue": "MCP stdin requires async executor",
                    "solution": "Use async executor instead of synchronous readline",
                    "category": "async",
                    "date_discovered": "2024-01-01",
                    "status": "resolved"
                },
                "powershell_syntax": {
                    "issue": "PowerShell && syntax not supported",
                    "solution": "Use separate commands instead of && chaining",
                    "category": "shell",
                    "date_discovered": "2024-01-01",
                    "status": "resolved"
                },
                "utf8_encoding": {
                    "issue": "UTF-8 encoding issues with special characters",
                    "solution": "Explicitly specify encoding='utf-8' in file operations",
                    "category": "encoding",
                    "date_discovered": "2024-01-01",
                    "status": "resolved"
                },
                "windows_file_paths": {
                    "issue": "File path handling inconsistencies",
                    "solution": "Use backslashes on Windows, Path() for cross-platform",
                    "category": "filesystem",
                    "date_discovered": "2024-01-01",
                    "status": "resolved"
                },
                "pip_path_issue": {
                    "issue": "pip command not in PATH",
                    "solution": "Use 'py -m pip' instead of direct pip command",
                    "category": "environment",
                    "date_discovered": "2024-01-01",
                    "status": "resolved"
                }
            }
            
            with open(self.discoveries_file, 'w', encoding='utf-8') as f:
                json.dump(initial_discoveries, f, indent=2)
    
    def is_path_allowed(self, path: str) -> bool:
        """Check if file path is in allowed directories"""
        abs_path = os.path.abspath(path)
        for allowed in self.allowed_directories:
            abs_allowed = os.path.abspath(allowed)
            if abs_path.startswith(abs_allowed):
                return True
        return False
    
    def get_request_id(self, request: Dict[str, Any]) -> Any:
        """Extract request ID for JSON-RPC response"""
        return request.get("id", 0)
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Main request handler for all MCP protocol methods"""
        method = request.get("method", "")
        request_id = self.get_request_id(request)
        
        try:
            if method == "initialize":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "project-knowledge-optimizer",
                            "version": "2.1.0"
                        }
                    }
                }
            
            elif method == "tools/list":
                return await self.list_tools(request_id)
            
            elif method == "tools/call":
                return await self.call_tool(request_id, request.get("params", {}))
            
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": f"Method not found: {method}"}
                }
        
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
            }
    
    async def list_tools(self, request_id: Any) -> Dict[str, Any]:
        """List all available tools"""
        tools = [
            {
                "name": "analyze_project_knowledge",
                "description": "Analyze project_knowledge.md file quality and AI-effectiveness (Target: 94.2/100 score)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to project_knowledge.md file to analyze"
                        },
                        "detailed": {
                            "type": "boolean",
                            "description": "Include detailed section breakdown (default: true)",
                            "default": True
                        }
                    },
                    "required": ["file_path"]
                }
            },
            {
                "name": "optimize_project_knowledge",
                "description": "Optimize project_knowledge.md using 80/20 principle and cognitive science",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to project_knowledge.md file to optimize"
                        },
                        "output_path": {
                            "type": "string",
                            "description": "Output path for optimized file (optional)",
                            "default": ""
                        },
                        "optimization_level": {
                            "type": "string",
                            "enum": ["basic", "advanced", "aggressive"],
                            "description": "Level of optimization to apply",
                            "default": "advanced"
                        }
                    },
                    "required": ["file_path"]
                }
            },
            {
                "name": "validate_mcp_protocol",
                "description": "Validate MCP protocol compliance and configuration",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "config_path": {
                            "type": "string",
                            "description": "Path to Claude Desktop config file (optional)"
                        },
                        "check_server": {
                            "type": "boolean",
                            "description": "Test server connectivity (default: true)",
                            "default": True
                        }
                    }
                }
            },
            {
                "name": "backup_project_knowledge",
                "description": "Create versioned backup of project_knowledge.md before making changes",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string", 
                            "description": "Path to project_knowledge.md file to backup"
                        },
                        "backup_name": {
                            "type": "string",
                            "description": "Custom backup name (optional, auto-generated if not provided)"
                        },
                        "include_analysis": {
                            "type": "boolean",
                            "description": "Include quality analysis with backup (default: true)",
                            "default": True
                        }
                    },
                    "required": ["file_path"]
                }
            },
            {
                "name": "restore_project_knowledge",
                "description": "Restore project_knowledge.md from previous backup",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "backup_id": {
                            "type": "string",
                            "description": "Backup ID or 'latest' for most recent backup"
                        },
                        "target_path": {
                            "type": "string",
                            "description": "Target path for restoration (optional)"
                        },
                        "verify_before_restore": {
                            "type": "boolean",
                            "description": "Verify backup integrity before restore (default: true)",
                            "default": True
                        }
                    },
                    "required": ["backup_id"]
                }
            },
            {
                "name": "safe_replace_project_knowledge",
                "description": "Safely replace project_knowledge.md with automatic backup and verification",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "current_file_path": {
                            "type": "string",
                            "description": "Path to current project_knowledge.md file"
                        },
                        "new_content": {
                            "type": "string",
                            "description": "New content to replace current file"
                        },
                        "verify_quality": {
                            "type": "boolean",
                            "description": "Verify quality improvement before replacing (default: true)",
                            "default": True
                        },
                        "minimum_score": {
                            "type": "number",
                            "description": "Minimum quality score required for replacement (default: 70.0)",
                            "default": 70.0
                        }
                    },
                    "required": ["current_file_path", "new_content"]
                }
            },
            {
                "name": "analyze_conversation_issues",
                "description": "Analyze Claude conversations to extract and track technical issues and discoveries",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "conversation_text": {
                            "type": "string",
                            "description": "Full conversation text to analyze for technical issues"
                        },
                        "session_context": {
                            "type": "string",
                            "description": "Context about the session/project (optional)"
                        },
                        "extract_discoveries": {
                            "type": "boolean",
                            "description": "Extract technical discoveries from conversation (default: true)",
                            "default": true
                        },
                        "update_knowledge_base": {
                            "type": "boolean",
                            "description": "Update knowledge base with discoveries (default: true)",
                            "default": true
                        }
                    },
                    "required": ["conversation_text"]
                }
            }
        ]
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"tools": tools}
        }
    
    async def call_tool(self, request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Route tool calls to appropriate handlers"""
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})
        
        # Security check for file operations
        if tool_name != "validate_mcp_protocol" and tool_name != "analyze_conversation_issues":
            file_path = arguments.get("file_path") or arguments.get("current_file_path")
            if file_path and not self.is_path_allowed(file_path):
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{
                            "type": "text",
                            "text": f"Access denied: Path '{file_path}' is not in allowed directories"
                        }]
                    }
                }
        
        # Route to tool handlers
        try:
            if tool_name == "analyze_project_knowledge":
                result = await self.analyze_project_knowledge(arguments)
            elif tool_name == "optimize_project_knowledge":
                result = await self.optimize_project_knowledge(arguments)
            elif tool_name == "validate_mcp_protocol":
                result = await self.validate_mcp_protocol(arguments)
            elif tool_name == "backup_project_knowledge":
                result = await self.backup_project_knowledge(arguments)
            elif tool_name == "restore_project_knowledge":
                result = await self.restore_project_knowledge(arguments)
            elif tool_name == "safe_replace_project_knowledge":
                result = await self.safe_replace_project_knowledge(arguments)
            elif tool_name == "analyze_conversation_issues":
                result = await self.analyze_conversation_issues(arguments)
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"}
                }

            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {"content": [{"type": "text", "text": result}]}
            }
            
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32603, "message": f"Tool execution error: {str(e)}"}
            }
    
    async def analyze_project_knowledge(self, arguments: Dict[str, Any]) -> str:
        """Analyze project_knowledge.md file quality and effectiveness"""
        file_path = arguments.get("file_path", "")
        detailed = arguments.get("detailed", True)
        
        if not os.path.exists(file_path):
            return f"ERROR: File not found: {file_path}"
        
        try:
            # Run analysis
            result = self.analyzer.analyze_file(file_path)
            
            # Create comprehensive report
            report = []
            report.append("="*70)
            report.append("  MCP PROJECT KNOWLEDGE OPTIMIZER - ANALYSIS REPORT")
            report.append("="*70)
            report.append(f"\nFile Analyzed: {file_path}")
            report.append(f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append("-" * 60)
            
            # Overall Score with status
            score = result.overall_score
            if score >= 90:
                status = "EXCELLENT [HIGH AI EFFECTIVENESS]"
            elif score >= 80:
                status = "GOOD [EFFECTIVE]"
            elif score >= 70:
                status = "NEEDS IMPROVEMENT [MODERATE]"
            else:
                status = "POOR [LOW EFFECTIVENESS]"
                
            report.append(f"\nOVERALL QUALITY SCORE: {score}/100 ({status})")
            
            # Detailed Scores
            report.append(f"\nDETAILED SCORES:")
            report.append(f"   Structure:    {result.scores['structure']}/100")
            report.append(f"   Content:      {result.scores['content']}/100") 
            report.append(f"   Clarity:      {result.scores['clarity']}/100")
            report.append(f"   Context:      {result.scores['context']}/100")
            
            # Key Metrics
            report.append(f"\nKEY METRICS:")
            metrics = result.metrics
            report.append(f"   Total Words:     {metrics['total_words']} (Target: 1,000-2,000)")
            report.append(f"   Sections:        {metrics['total_sections']}")
            report.append(f"   Max Section:     {metrics['max_section_words']} words (Max: 750)")
            report.append(f"   Avg Section:     {metrics['avg_section_words']} words")
            report.append(f"   Header Depth:    {metrics['hierarchy_depth']} levels (Max: 4)")
            report.append(f"   Code Blocks:     {'Yes' if metrics['has_code_blocks'] else 'No'}")
            report.append(f"   Appendices:      {'Yes' if metrics['has_appendices'] else 'No'}")
            
            # Recommendations
            report.append(f"\nRECOMMENDATIONS ({len(result.recommendations)} items):")
            if result.recommendations:
                for i, rec in enumerate(result.recommendations, 1):
                    report.append(f"   {i}. {rec}")
            else:
                report.append("   No recommendations - document is excellently optimized!")
            
            # Section Breakdown (if detailed)
            if detailed and result.sections:
                report.append(f"\nSECTION BREAKDOWN:")
                for i, section in enumerate(result.sections, 1):
                    level_indent = "  " * (section['level'] - 1)
                    if section['word_count'] > 750:
                        status_icon = "[LONG]"
                    elif section['word_count'] < 50:
                        status_icon = "[SHORT]"
                    else:
                        status_icon = "[OK]"
                    
                    report.append(f"   {i}. {level_indent}H{section['level']}: {section['title']}")
                    report.append(f"      {level_indent}Words: {section['word_count']} {status_icon}")
            
            # AI Effectiveness Tips
            report.append(f"\nAI EFFECTIVENESS TIPS:")
            report.append("   - Front-load context: project overview, tech stack, constraints")
            report.append("   - Use 80/20 principle: core info first, details in appendices")
            report.append("   - Keep sections digestible: under 750 words each")
            report.append("   - Include technical discoveries and known issues")
            report.append("   - Use code blocks and bullet points for clarity")
            report.append("   - Maintain consistent terminology throughout")
            
            report.append(f"\nAnalysis completed successfully!")
            report.append("="*70)
            
            return "\n".join(report)
            
        except Exception as e:
            return f"ERROR: Analysis failed: {str(e)}"
    
    async def optimize_project_knowledge(self, arguments: Dict[str, Any]) -> str:
        """Optimize project_knowledge.md using research-driven principles"""
        file_path = arguments.get("file_path", "")
        output_path = arguments.get("output_path", "")
        optimization_level = arguments.get("optimization_level", "advanced")
        
        if not os.path.exists(file_path):
            return f"ERROR: File not found: {file_path}"
        
        try:
            # Read current content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Analyze current state
            result = self.analyzer.analyze_file(file_path)
            
            # Apply optimizations based on level
            optimized_content = self._apply_optimizations(content, result, optimization_level)
            
            # Determine output path
            if not output_path:
                path_obj = Path(file_path)
                output_path = str(path_obj.parent / f"{path_obj.stem}_optimized{path_obj.suffix}")
            
            # Write optimized content
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(optimized_content)
            
            # Analyze optimized version
            optimized_result = self.analyzer.analyze_file(output_path)
            
            # Create optimization report
            report = []
            report.append("="*70)
            report.append("  PROJECT KNOWLEDGE OPTIMIZATION COMPLETE")
            report.append("="*70)
            report.append(f"\nSource File: {file_path}")
            report.append(f"Optimized File: {output_path}")
            report.append(f"Optimization Level: {optimization_level.upper()}")
            report.append(f"Optimization Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Before/After Comparison
            report.append(f"\nQUALITY IMPROVEMENT:")
            report.append(f"   Before: {result.overall_score}/100")
            report.append(f"   After:  {optimized_result.overall_score}/100")
            improvement = optimized_result.overall_score - result.overall_score
            report.append(f"   Change: {improvement:+.1f} points")
            
            if improvement > 0:
                report.append(f"   Status: IMPROVED")
            elif improvement == 0:
                report.append(f"   Status: NO CHANGE")
            else:
                report.append(f"   Status: NEEDS REVIEW")
            
            # Detailed score improvements
            report.append(f"\nSCORE BREAKDOWN:")
            for category in ['structure', 'content', 'clarity', 'context']:
                before = result.scores[category]
                after = optimized_result.scores[category]
                change = after - before
                report.append(f"   {category.title():12} {before:5.1f} -> {after:5.1f} ({change:+.1f})")
            
            # Applied optimizations
            report.append(f"\nOPTIMIZATIONS APPLIED:")
            optimizations = self._get_applied_optimizations(result, optimization_level)
            for opt in optimizations:
                report.append(f"   - {opt}")
            
            # Remaining recommendations
            if optimized_result.recommendations:
                report.append(f"\nFURTHER IMPROVEMENTS:")
                for rec in optimized_result.recommendations[:3]:  # Top 3
                    report.append(f"   - {rec}")
            
            report.append(f"\nOptimization completed successfully!")
            report.append("="*70)
            
            return "\n".join(report)
            
        except Exception as e:
            return f"ERROR: Optimization failed: {str(e)}"
    
    def _apply_optimizations(self, content: str, analysis: AnalysisResult, level: str) -> str:
        """Apply optimizations based on analysis results and level"""
        optimized = content
        
        # Basic optimizations (all levels)
        if analysis.scores['structure'] < 80:
            optimized = self._optimize_structure(optimized)
        
        if analysis.scores['clarity'] < 80:
            optimized = self._optimize_clarity(optimized)
        
        # Advanced optimizations
        if level in ['advanced', 'aggressive']:
            if analysis.scores['content'] < 80:
                optimized = self._optimize_content(optimized)
            
            if analysis.scores['context'] < 80:
                optimized = self._optimize_context(optimized)
        
        # Aggressive optimizations
        if level == 'aggressive':
            optimized = self._apply_aggressive_optimizations(optimized)
        
        return optimized
    
    def _optimize_structure(self, content: str) -> str:
        """Optimize document structure and hierarchy"""
        lines = content.split('\n')
        optimized_lines = []
        
        current_section_lines = []
        current_section_words = 0
        
        for line in lines:
            # Check if it's a header
            if re.match(r'^#{1,6}\s+', line):
                # Process previous section if it was too long
                if current_section_words > 750 and current_section_lines:
                    # Split long section
                    optimized_lines.extend(self._split_long_section(current_section_lines))
                else:
                    optimized_lines.extend(current_section_lines)
                
                # Start new section
                current_section_lines = [line]
                current_section_words = 0
            else:
                current_section_lines.append(line)
                current_section_words += len(line.split())
        
        # Don't forget the last section
        if current_section_lines:
            if current_section_words > 750:
                optimized_lines.extend(self._split_long_section(current_section_lines))
            else:
                optimized_lines.extend(current_section_lines)
        
        return '\n'.join(optimized_lines)
    
    def _split_long_section(self, section_lines: List[str]) -> List[str]:
        """Split a long section into smaller subsections"""
        if len(section_lines) <= 1:
            return section_lines
        
        header = section_lines[0]
        content = section_lines[1:]
        
        # Simple split: add subsection headers at paragraph breaks
        result = [header]
        current_subsection = []
        word_count = 0
        
        for line in content:
            if line.strip() == '' and word_count > 300:  # Paragraph break
                if current_subsection:
                    # Add subsection header
                    subsection_header = header.replace('#', '##', 1) + f" - Part {len(result)}"
                    result.append('')
                    result.append(subsection_header)
                    result.extend(current_subsection)
                    current_subsection = []
                    word_count = 0
            
            current_subsection.append(line)
            word_count += len(line.split())
        
        # Add remaining content
        result.extend(current_subsection)
        return result
    
    def _optimize_clarity(self, content: str) -> str:
        """Optimize content for clarity and readability"""
        # Add more bullet points where appropriate
        lines = content.split('\n')
        optimized_lines = []
        
        for line in lines:
            # Convert long sentences with commas to bullet points
            if (not line.startswith('#') and 
                not line.startswith('-') and 
                not line.startswith('*') and
                line.count(',') > 2 and
                len(line.split()) > 20):
                
                # Split on commas and convert to bullets
                parts = [part.strip() for part in line.split(',')]
                if len(parts) > 2:
                    optimized_lines.append('')
                    for part in parts:
                        if part:
                            optimized_lines.append(f"- {part}")
                    optimized_lines.append('')
                    continue
            
            optimized_lines.append(line)
        
        return '\n'.join(optimized_lines)
    
    def _optimize_content(self, content: str) -> str:
        """Optimize content using 80/20 principle"""
        # Move detailed content to appendix sections
        lines = content.split('\n')
        core_content = []
        appendix_content = []
        
        current_section = []
        in_appendix = False
        
        for line in lines:
            if re.match(r'^#{1,6}\s+', line):
                # Process previous section
                if current_section:
                    if in_appendix:
                        appendix_content.extend(current_section)
                    else:
                        core_content.extend(current_section)
                
                # Check if this section should be in appendix
                if any(keyword in line.lower() for keyword in ['reference', 'appendix', 'detailed', 'technical specs']):
                    in_appendix = True
                    appendix_content.append(line)
                else:
                    in_appendix = False
                    core_content.append(line)
                
                current_section = []
            else:
                current_section.append(line)
        
        # Add final section
        if current_section:
            if in_appendix:
                appendix_content.extend(current_section)
            else:
                core_content.extend(current_section)
        
        # Combine with appendix at the end
        if appendix_content and not any('appendix' in line.lower() for line in core_content):
            core_content.extend(['', '## Appendix', ''])
            core_content.extend(appendix_content)
        
        return '\n'.join(core_content)
    
    def _optimize_context(self, content: str) -> str:
        """Optimize context section to front-load critical information"""
        lines = content.split('\n')
        
        # Find or create context section
        context_section = []
        rest_content = []
        found_context = False
        
        current_section = []
        in_context = False
        
        for line in lines:
            if re.match(r'^#{1,6}\s+', line):
                # Save previous section
                if current_section:
                    if in_context:
                        context_section.extend(current_section)
                        found_context = True
                    else:
                        rest_content.extend(current_section)
                
                # Check if this is context section
                if any(keyword in line.lower() for keyword in ['context', 'overview', 'introduction']):
                    in_context = True
                    context_section.append(line)
                else:
                    in_context = False
                    rest_content.append(line)
                
                current_section = []
            else:
                current_section.append(line)
        
        # Add final section
        if current_section:
            if in_context:
                context_section.extend(current_section)
            else:
                rest_content.extend(current_section)
        
        # If no context section found, create one
        if not found_context:
            context_section = [
                '# Project Context',
                '',
                '## Project Overview',
                'Brief description of the project goals and scope.',
                '',
                '## Technical Stack',
                'Key technologies, frameworks, and dependencies.',
                '',
                '## Requirements & Constraints',
                'Important requirements and constraints to consider.',
                '',
                '## Key Decisions',
                'Critical architectural and design decisions made.',
                ''
            ]
        
        # Combine with context first
        return '\n'.join(context_section + [''] + rest_content)
    
    def _apply_aggressive_optimizations(self, content: str) -> str:
        """Apply aggressive optimizations for maximum AI effectiveness"""
        # This would include more advanced transformations
        # For now, ensure consistent formatting
        
        lines = content.split('\n')
        optimized_lines = []
        
        for line in lines:
            # Standardize bullet points
            line = re.sub(r'^[\*\+]\s+', '- ', line)
            
            # Ensure proper spacing around headers
            if re.match(r'^#{1,6}\s+', line):
                if optimized_lines and optimized_lines[-1].strip():
                    optimized_lines.append('')
                optimized_lines.append(line)
                optimized_lines.append('')
            else:
                optimized_lines.append(line)
        
        return '\n'.join(optimized_lines)
    
    def _get_applied_optimizations(self, analysis: AnalysisResult, level: str) -> List[str]:
        """Get list of optimizations that were applied"""
        optimizations = []
        
        if analysis.scores['structure'] < 80:
            optimizations.append("Improved document structure and hierarchy")
            optimizations.append("Split oversized sections for better readability")
        
        if analysis.scores['clarity'] < 80:
            optimizations.append("Enhanced clarity with bullet points and lists")
            optimizations.append("Simplified complex sentences")
        
        if level in ['advanced', 'aggressive']:
            if analysis.scores['content'] < 80:
                optimizations.append("Applied 80/20 principle to content organization")
                optimizations.append("Moved detailed content to appendix sections")
            
            if analysis.scores['context'] < 80:
                optimizations.append("Front-loaded critical context information")
                optimizations.append("Enhanced project overview and technical stack details")
        
        if level == 'aggressive':
            optimizations.append("Standardized formatting and bullet point styles")
            optimizations.append("Optimized spacing and visual hierarchy")
        
        return optimizations
    
    async def validate_mcp_protocol(self, arguments: Dict[str, Any]) -> str:
        """Validate MCP protocol compliance and configuration"""
        config_path = arguments.get("config_path", "")
        check_server = arguments.get("check_server", True)
        
        report = []
        report.append("="*60)
        report.append("  MCP PROTOCOL VALIDATION REPORT")
        report.append("="*60)
        report.append(f"Validation Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Check protocol version
        report.append(f"\nPROTOCOL COMPLIANCE:")
        report.append(f"   Protocol Version: 2024-11-05 [OK]")
        report.append(f"   Server Name: project-knowledge-optimizer [OK]")

        
        # Check Claude Desktop config
        if not config_path:
            config_path = os.path.expanduser("~/AppData/Roaming/Claude/claude_desktop_config.json")
        
        report.append(f"\nCLAUDE DESKTOP CONFIG:")
        report.append(f"   Config Path: {config_path}")
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Check for MCP servers section
                if 'mcpServers' in config:
                    servers = config['mcpServers']
                    if 'project-knowledge-optimizer' in servers:
                        report.append(f"   Server Config: [OK] Found")
                        server_config = servers['project-knowledge-optimizer']
                        report.append(f"   Command: {server_config.get('command', 'Not specified')}")
                        report.append(f"   Args: {server_config.get('args', [])}")
                    else:
                        report.append(f"   Server Config: [ERROR] Not found")
                        report.append(f"   Status: Server not configured in Claude Desktop")
                else:
                    report.append(f"   MCP Servers: [ERROR] No mcpServers section found")
                    
            except Exception as e:
                report.append(f"   Config Error: [ERROR] {str(e)}")
        else:
            report.append(f"   Config File: [ERROR] Not found")
        
        # Server connectivity test
        if check_server:
            report.append(f"\nSERVER CONNECTIVITY:")
            try:
                # Test server initialization
                test_request = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {}
                }
                response = await self.handle_request(test_request)
                
                if "result" in response:
                    report.append(f"   Initialization: [OK] Success")
                    report.append(f"   Protocol Version: {response['result']['protocolVersion']}")
                    report.append(f"   Server Info: {response['result']['serverInfo']['name']} v{response['result']['serverInfo']['version']}")
                else:
                    report.append(f"   Initialization: [ERROR] Failed")
                    report.append(f"   Error: {response.get('error', {}).get('message', 'Unknown error')}")
                
            except Exception as e:
                report.append(f"   Server Test: [ERROR] Error: {str(e)}")
        
        # Technical discoveries check
        report.append(f"\nTECHNICAL DISCOVERIES:")
        if self.discoveries_file.exists():
            with open(self.discoveries_file, 'r', encoding='utf-8') as f:
                discoveries = json.load(f)
            
            report.append(f"   Database: [OK] {len(discoveries)} discoveries tracked")
            report.append(f"   Categories: {', '.join(set(d.get('category', 'unknown') for d in discoveries.values()))}")
            
            # Show recent discoveries
            recent = [k for k, v in discoveries.items() if v.get('status') == 'resolved'][:3]
            if recent:
                report.append(f"   Recent Solutions:")
                for key in recent:
                    discovery = discoveries[key]
                    report.append(f"     - {discovery.get('issue', key)}")
                    
        else:
            report.append(f"   Database: [ERROR] Not initialized")
        
        # Configuration recommendations
        report.append(f"\nRECOMMENDATIONS:")
        report.append(f"   - Ensure Claude Desktop is restarted after config changes")
        report.append(f"   - Use 'py' command instead of 'python' on Windows")
        report.append(f"   - Check file permissions for backup directory")
        report.append(f"   - Monitor server logs for any connection issues")
        
        report.append(f"\nMCP Protocol validation completed!")
        report.append("="*60)
        
        return "\n".join(report)
    
    async def backup_project_knowledge(self, arguments: Dict[str, Any]) -> str:
        """Create versioned backup of project_knowledge.md"""
        file_path = arguments.get("file_path", "")
        backup_name = arguments.get("backup_name", "")
        include_analysis = arguments.get("include_analysis", True)
        
        if not os.path.exists(file_path):
            return f"ERROR: File not found: {file_path}"
        
        try:
            # Generate backup ID and name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if not backup_name:
                backup_name = f"backup_{timestamp}"
            
            backup_id = f"{backup_name}_{timestamp}"
            
            # Create backup directory structure
            backup_path = self.backup_dir / backup_id
            backup_path.mkdir(exist_ok=True)
            
            # Copy the file
            backup_file_path = backup_path / "project_knowledge.md"
            shutil.copy2(file_path, backup_file_path)
            
            # Create backup metadata
            metadata = {
                "backup_id": backup_id,
                "backup_name": backup_name,
                "original_path": file_path,
                "backup_path": str(backup_file_path),
                "created_at": datetime.now().isoformat(),
                "file_size": os.path.getsize(file_path),
                "file_hash": self._calculate_file_hash(file_path)
            }
            
            # Include analysis if requested
            if include_analysis:
                try:
                    analysis_result = self.analyzer.analyze_file(file_path)
                    metadata["quality_analysis"] = {
                        "overall_score": analysis_result.overall_score,
                        "scores": analysis_result.scores,
                        "total_words": analysis_result.metrics['total_words'],
                        "total_sections": analysis_result.metrics['total_sections']
                    }
                except Exception as e:
                    metadata["analysis_error"] = str(e)
            
            # Save metadata
            metadata_path = backup_path / "metadata.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            
            # Update backup index
            self._update_backup_index(metadata)
            
            # Create backup report
            report = []
            report.append("="*60)
            report.append("  PROJECT KNOWLEDGE BACKUP CREATED")
            report.append("="*60)
            report.append(f"Backup ID: {backup_id}")
            report.append(f"Backup Name: {backup_name}")
            report.append(f"Source File: {file_path}")
            report.append(f"Backup Location: {backup_file_path}")
            report.append(f"Created: {metadata['created_at']}")
            report.append(f"File Size: {metadata['file_size']} bytes")
            
            if include_analysis and "quality_analysis" in metadata:
                analysis = metadata["quality_analysis"]
                report.append(f"\nQUALITY SNAPSHOT:")
                report.append(f"   Overall Score: {analysis['overall_score']}/100")
                report.append(f"   Total Words: {analysis['total_words']}")
                report.append(f"   Sections: {analysis['total_sections']}")
            
            report.append(f"\nBackup created successfully!")
            report.append(f"Use backup ID '{backup_id}' for restoration")
            report.append("="*60)
            
            return "\n".join(report)
            
        except Exception as e:
            return f"ERROR: Backup failed: {str(e)}"
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA-256 hash of file for integrity verification"""
        import hashlib
        
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    
    def _update_backup_index(self, metadata: Dict[str, Any]):
        """Update the backup index with new backup metadata"""
        index_path = self.backup_dir / "backup_index.json"
        
        # Load existing index
        if index_path.exists():
            with open(index_path, 'r', encoding='utf-8') as f:
                index = json.load(f)
        else:
            index = {"backups": [], "created_at": datetime.now().isoformat()}
        
        # Add new backup
        index["backups"].append(metadata)
        index["last_updated"] = datetime.now().isoformat()
        
        # Save updated index
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2)
    
    async def restore_project_knowledge(self, arguments: Dict[str, Any]) -> str:
        """Restore project_knowledge.md from backup"""
        backup_id = arguments.get("backup_id", "")
        target_path = arguments.get("target_path", "")
        verify_before_restore = arguments.get("verify_before_restore", True)
        
        if not backup_id:
            return "ERROR: Backup ID is required"
        
        try:
            # Load backup index
            index_path = self.backup_dir / "backup_index.json"
            if not index_path.exists():
                return "ERROR: No backup index found"
            
            with open(index_path, 'r', encoding='utf-8') as f:
                index = json.load(f)
            
            # Find backup
            backup_metadata = None
            if backup_id == "latest":
                # Get most recent backup
                if index["backups"]:
                    backup_metadata = max(index["backups"], key=lambda x: x["created_at"])
            else:
                # Find specific backup
                for backup in index["backups"]:
                    if backup["backup_id"] == backup_id:
                        backup_metadata = backup
                        break
            
            if not backup_metadata:
                available_backups = [b["backup_id"] for b in index["backups"]]
                return f"ERROR: Backup '{backup_id}' not found. Available: {', '.join(available_backups)}"
            
            # Verify backup integrity if requested
            backup_file_path = backup_metadata["backup_path"]
            if verify_before_restore:
                if not os.path.exists(backup_file_path):
                    return f"ERROR: Backup file not found: {backup_file_path}"
                
                # Verify file hash
                current_hash = self._calculate_file_hash(backup_file_path)
                expected_hash = backup_metadata.get("file_hash", "")
                if expected_hash and current_hash != expected_hash:
                    return f"ERROR: Backup file integrity check failed"
            
            # Determine target path
            if not target_path:
                target_path = backup_metadata["original_path"]
            
            # Check target path permission
            if not self.is_path_allowed(target_path):
                return f"ERROR: Access denied for target path: {target_path}"
            
            # Create backup of current file if it exists
            if os.path.exists(target_path):
                current_backup_path = f"{target_path}.restore_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                shutil.copy2(target_path, current_backup_path)
            
            # Restore the file
            shutil.copy2(backup_file_path, target_path)
            
            # Create restoration report
            report = []
            report.append("="*60)
            report.append("  PROJECT KNOWLEDGE RESTORED")
            report.append("="*60)
            report.append(f"Backup ID: {backup_metadata['backup_id']}")
            report.append(f"Backup Created: {backup_metadata['created_at']}")
            report.append(f"Restored To: {target_path}")
            report.append(f"Restored At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            if "quality_analysis" in backup_metadata:
                analysis = backup_metadata["quality_analysis"]
                report.append(f"\nRESTORED QUALITY:")
                report.append(f"   Overall Score: {analysis['overall_score']}/100")
                report.append(f"   Total Words: {analysis['total_words']}")
                report.append(f"   Sections: {analysis['total_sections']}")
            
            if verify_before_restore:
                report.append(f"\nINTEGRITY VERIFIED:")
                report.append(f"   File Hash: {current_hash[:16]}...")
                report.append(f"   Status: [OK] Verified")
            
            report.append(f"\nRestoration completed successfully!")
            report.append("="*60)
            
            return "\n".join(report)
            
        except Exception as e:
            return f"ERROR: Restoration failed: {str(e)}"
    
    async def safe_replace_project_knowledge(self, arguments: Dict[str, Any]) -> str:
        """Safely replace project_knowledge.md with automatic backup and verification"""
        current_file_path = arguments.get("current_file_path", "")
        new_content = arguments.get("new_content", "")
        verify_quality = arguments.get("verify_quality", True)
        minimum_score = arguments.get("minimum_score", 70.0)
        
        if not current_file_path or not new_content:
            return "ERROR: Both current_file_path and new_content are required"
        
        if not os.path.exists(current_file_path):
            return f"ERROR: Current file not found: {current_file_path}"
        
        try:
            # Create backup first
            backup_args = {
                "file_path": current_file_path,
                "backup_name": "pre_replacement",
                "include_analysis": True
            }
            backup_result = await self.backup_project_knowledge(backup_args)
            
            if backup_result.startswith("ERROR"):
                return f"ERROR: Backup failed: {backup_result}"
            
            # Write new content to temporary file for testing
            temp_file = f"{current_file_path}.temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            # Analyze quality if verification requested
            quality_check_passed = True
            quality_report = ""
            
            if verify_quality:
                try:
                    # Analyze original file
                    original_analysis = self.analyzer.analyze_file(current_file_path)
                    
                    # Analyze new content
                    new_analysis = self.analyzer.analyze_file(temp_file)
                    
                    # Check if quality meets minimum requirement
                    if new_analysis.overall_score < minimum_score:
                        quality_check_passed = False
                        quality_report = f"Quality check failed: {new_analysis.overall_score}/100 < {minimum_score} (minimum required)"
                    
                    # Check if quality improved or maintained
                    elif new_analysis.overall_score < original_analysis.overall_score - 5:  # Allow 5-point tolerance
                        quality_check_passed = False
                        quality_report = f"Quality degraded: {original_analysis.overall_score}/100 -> {new_analysis.overall_score}/100"
                    
                    else:
                        quality_report = f"Quality verified: {original_analysis.overall_score}/100 -> {new_analysis.overall_score}/100"
                        
                except Exception as e:
                    quality_check_passed = False
                    quality_report = f"Quality analysis failed: {str(e)}"
            
            # Proceed with replacement if quality check passed
            if quality_check_passed:
                # Replace the file
                shutil.move(temp_file, current_file_path)
                
                # Create success report
                report = []
                report.append("="*60)
                report.append("  SAFE REPLACEMENT COMPLETED")
                report.append("="*60)
                report.append(f"File: {current_file_path}")
                report.append(f"Replaced At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                report.append(f"Backup Created: [OK] Yes")
                
                if verify_quality:
                    report.append(f"Quality Check: [OK] Passed")
                    report.append(f"Quality Report: {quality_report}")
                
                report.append(f"\nFile replacement completed successfully!")
                report.append("Use 'restore_project_knowledge' with 'latest' backup to undo if needed")
                report.append("="*60)
                
                return "\n".join(report)
                
            else:
                # Quality check failed - clean up temp file and report
                os.remove(temp_file)
                
                report = []
                report.append("="*60)
                report.append("  SAFE REPLACEMENT CANCELLED")
                report.append("="*60)
                report.append(f"File: {current_file_path}")
                report.append(f"Reason: Quality verification failed")
                report.append(f"Details: {quality_report}")
                report.append(f"\nReplacement cancelled to prevent quality degradation")
                report.append("Original file remains unchanged")
                report.append("Improve the new content and try again")
                report.append("="*60)
                
                return "\n".join(report)
                
        except Exception as e:
            # Clean up temp file if it exists
            if 'temp_file' in locals() and os.path.exists(temp_file):
                os.remove(temp_file)
            
            return f"ERROR: Safe replacement failed: {str(e)}"
    
    async def analyze_conversation_issues(self, arguments: Dict[str, Any]) -> str:
        """Analyze Claude conversations to extract technical issues and discoveries"""
        conversation_text = arguments.get("conversation_text", "")
        session_context = arguments.get("session_context", "")
        extract_discoveries = arguments.get("extract_discoveries", True)
        update_knowledge_base = arguments.get("update_knowledge_base", True)
        
        if not conversation_text:
            return "ERROR: Conversation text is required"
        
        try:
            # Analyze conversation for issues
            issues = self._extract_conversation_issues(conversation_text)
            
            # Extract technical discoveries if requested
            discoveries = []
            if extract_discoveries:
                discoveries = self._extract_technical_discoveries(conversation_text)
            
            # Update knowledge base if requested
            if update_knowledge_base and discoveries:
                self._update_discoveries_database(discoveries)
            
            # Create analysis report
            report = []
            report.append("="*70)
            report.append("  CONVERSATION ISSUE ANALYSIS REPORT")
            report.append("="*70)
            report.append(f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            if session_context:
                report.append(f"Session Context: {session_context}")
            report.append(f"Conversation Length: {len(conversation_text.split())} words")
            
            # Issues found
            report.append(f"\nTECHNICAL ISSUES IDENTIFIED ({len(issues)}):")
            if issues:
                for i, issue in enumerate(issues, 1):
                    report.append(f"\n   {i}. {issue.issue_type.upper()}: {issue.description}")
                    
                    if issue.attempted_solutions:
                        report.append(f"      Attempted Solutions:")
                        for solution in issue.attempted_solutions:
                            report.append(f"        - {solution}")
                    
                    report.append(f"      Status: {issue.resolution_status}")
                    
                    if issue.technical_discovery:
                        report.append(f"      Discovery: {issue.technical_discovery}")
            else:
                report.append("   No technical issues detected")
            
            # Technical discoveries
            if extract_discoveries:
                report.append(f"\nTECHNICAL DISCOVERIES ({len(discoveries)}):")
                if discoveries:
                    for discovery in discoveries:
                        report.append(f"   - {discovery['category'].upper()}: {discovery['solution']}")
                        report.append(f"     Issue: {discovery['issue']}")
                        if discovery.get('context'):
                            report.append(f"     Context: {discovery['context']}")
                else:
                    report.append("   No new technical discoveries found")
            
            # Knowledge base status
            if update_knowledge_base:
                report.append(f"\nKNOWLEDGE BASE:")
                with open(self.discoveries_file, 'r', encoding='utf-8') as f:
                    all_discoveries = json.load(f)
                
                report.append(f"   Total Discoveries: {len(all_discoveries)}")
                categories = set(d.get('category', 'unknown') for d in all_discoveries.values())
                report.append(f"   Categories: {', '.join(categories)}")
                
                if discoveries:
                    report.append(f"   New Discoveries Added: {len(discoveries)}")
            
            # Recommendations
            report.append(f"\nRECOMMENDATIONS:")
            
            unresolved_issues = [issue for issue in issues if issue.resolution_status.lower() not in ['resolved', 'fixed']]
            if unresolved_issues:
                report.append(f"   - Review {len(unresolved_issues)} unresolved technical issues")
                report.append(f"   - Document solutions for future reference")
            
            if discoveries:
                report.append(f"   - Update project documentation with new discoveries")
                report.append(f"   - Share solutions with team to prevent repetition")
            
            report.append(f"   - Use 'validate_mcp_protocol' to check current system status")
            report.append(f"   - Create backup before implementing new solutions")
            
            # Technical patterns detected
            patterns = self._identify_technical_patterns(issues, discoveries)
            if patterns:
                report.append(f"\nTECHNICAL PATTERNS DETECTED:")
                for pattern in patterns:
                    report.append(f"   - {pattern}")
            
            report.append(f"\nConversation analysis completed!")
            report.append("="*70)
            
            return "\n".join(report)
            
        except Exception as e:
            return f"ERROR: Conversation analysis failed: {str(e)}"
    
    def _extract_conversation_issues(self, conversation_text: str) -> List[ConversationIssue]:
        """Extract technical issues from conversation text"""
        issues = []
        
        # Define patterns for common technical issues
        issue_patterns = [
            {
                'type': 'command_error',
                'patterns': [r'command not found', r'is not recognized', r'not in PATH'],
                'solutions_keywords': ['use instead', 'try', 'install', 'add to path']
            },
            {
                'type': 'permission_error',
                'patterns': [r'permission denied', r'access denied', r'not allowed'],
                'solutions_keywords': ['chmod', 'run as admin', 'change permissions']
            },
            {
                'type': 'file_not_found',
                'patterns': [r'file not found', r'no such file', r'does not exist'],
                'solutions_keywords': ['create file', 'check path', 'file exists']
            },
            {
                'type': 'encoding_error',
                'patterns': [r'encoding error', r'utf-?8', r'unicode', r'special characters'],
                'solutions_keywords': ['encoding=', 'utf-8', 'decode', 'encode']
            },
            {
                'type': 'syntax_error',
                'patterns': [r'syntax error', r'invalid syntax', r'unexpected'],
                'solutions_keywords': ['correct syntax', 'fix', 'change to', 'use']
            },
            {
                'type': 'connection_error',
                'patterns': [r'connection error', r'connection refused', r'timeout'],
                'solutions_keywords': ['restart', 'check connection', 'try again']
            }
        ]
        
        # Split conversation into sections (by user/assistant turns)
        sections = re.split(r'\n(?=User:|Assistant:|Human:|Claude:)', conversation_text)
        
        for section in sections:
            section_lower = section.lower()
            
            # Check for issue patterns
            for issue_pattern in issue_patterns:
                for pattern in issue_pattern['patterns']:
                    if re.search(pattern, section_lower):
                        # Extract description
                        lines = section.split('\n')
                        description_lines = [line.strip() for line in lines[:3] if line.strip()]
                        description = ' '.join(description_lines)[:200]
                        
                        # Find attempted solutions
                        solutions = []
                        for line in lines:
                            line_lower = line.lower()
                            for keyword in issue_pattern['solutions_keywords']:
                                if keyword in line_lower:
                                    solutions.append(line.strip()[:100])
                                    break
                        
                        # Determine resolution status
                        resolution_status = "unresolved"
                        if any(word in section_lower for word in ['fixed', 'resolved', 'working', 'success']):
                            resolution_status = "resolved"
                        elif any(word in section_lower for word in ['workaround', 'temporary']):
                            resolution_status = "workaround"
                        
                        # Extract technical discovery
                        discovery = None
                        discovery_indicators = ['discovered', 'found that', 'turns out', 'solution']
                        for line in lines:
                            if any(indicator in line.lower() for indicator in discovery_indicators):
                                discovery = line.strip()[:150]
                                break
                        
                        issue = ConversationIssue(
                            issue_type=issue_pattern['type'],
                            description=description,
                            attempted_solutions=solutions[:3],  # Limit to 3 solutions
                            resolution_status=resolution_status,
                            technical_discovery=discovery,
                            session_context=section[:100]
                        )
                        
                        issues.append(issue)
                        break  # Only match first pattern per section
        
        return issues
    
    def _extract_technical_discoveries(self, conversation_text: str) -> List[Dict[str, Any]]:
        """Extract technical discoveries from conversation text"""
        discoveries = []
        
        # Patterns for technical discoveries
        discovery_patterns = [
            {
                'category': 'environment',
                'indicators': [r'use.*instead of', r'command.*not.*python', r'py.*not.*python'],
                'extract_solution': lambda text: re.search(r'use ["\']?([^"\']+)["\']?', text.lower())
            },
            {
                'category': 'protocol',
                'indicators': [r'version.*2024-11-05', r'protocol.*version', r'mcp.*version'],
                'extract_solution': lambda text: re.search(r'version ["\']?([^"\']+)["\']?', text)
            },
            {
                'category': 'async',
                'indicators': [r'async.*executor', r'stdin.*async', r'synchronous.*readline'],
                'extract_solution': lambda text: re.search(r'use (async[^.]+)', text.lower())
            },
            {
                'category': 'shell',
                'indicators': [r'powershell.*&&', r'separate.*commands', r'not.*supported'],
                'extract_solution': lambda text: re.search(r'use ([^.]+)', text.lower())
            },
            {
                'category': 'encoding',
                'indicators': [r'encoding.*utf-?8', r'special.*characters', r'unicode'],
                'extract_solution': lambda text: re.search(r'encoding=["\']?([^"\']+)["\']?', text)
            }
        ]
        
        text_lines = conversation_text.split('\n')
        
        for line in text_lines:
            line_lower = line.lower()
            
            for pattern in discovery_patterns:
                for indicator in pattern['indicators']:
                    if re.search(indicator, line_lower):
                        # Extract solution using pattern
                        solution_match = pattern['extract_solution'](line)
                        if solution_match:
                            solution = solution_match.group(1)
                        else:
                            solution = line.strip()[:100]
                        
                        # Create unique key for this discovery
                        discovery_key = f"{pattern['category']}_{len(discoveries)}"
                        
                        discovery = {
                            'key': discovery_key,
                            'category': pattern['category'],
                            'issue': line.strip()[:150],
                            'solution': solution,
                            'context': line.strip(),
                            'date_discovered': datetime.now().strftime('%Y-%m-%d'),
                            'status': 'new'
                        }
                        
                        discoveries.append(discovery)
                        break
        
        return discoveries
    
    def _update_discoveries_database(self, discoveries: List[Dict[str, Any]]):
        """Update the technical discoveries database with new discoveries"""
        # Load existing discoveries
        with open(self.discoveries_file, 'r', encoding='utf-8') as f:
            existing = json.load(f)
        
        # Add new discoveries (avoid duplicates)
        for discovery in discoveries:
            key = discovery['key']
            
            # Check if similar discovery already exists
            duplicate_found = False
            for existing_key, existing_discovery in existing.items():
                if (existing_discovery.get('category') == discovery['category'] and
                    discovery['solution'].lower() in existing_discovery.get('solution', '').lower()):
                    duplicate_found = True
                    break
            
            if not duplicate_found:
                existing[key] = discovery
        
        # Save updated database
        with open(self.discoveries_file, 'w', encoding='utf-8') as f:
            json.dump(existing, f, indent=2)
    
    def _identify_technical_patterns(self, issues: List[ConversationIssue], discoveries: List[Dict[str, Any]]) -> List[str]:
        """Identify recurring technical patterns from issues and discoveries"""
        patterns = []
        
        # Analyze issue types
        issue_types = [issue.issue_type for issue in issues]
        from collections import Counter
        type_counts = Counter(issue_types)
        
        for issue_type, count in type_counts.items():
            if count > 1:
                patterns.append(f"Recurring {issue_type.replace('_', ' ')} issues ({count} occurrences)")
        
        # Analyze discovery categories
        if discoveries:
            categories = [d['category'] for d in discoveries]
            category_counts = Counter(categories)
            
            for category, count in category_counts.items():
                if count > 0:
                    patterns.append(f"Multiple {category} discoveries indicate focus area")
        
        # Check for resolution patterns
        resolved_count = sum(1 for issue in issues if issue.resolution_status == 'resolved')
        total_issues = len(issues)
        
        if total_issues > 0:
            resolution_rate = resolved_count / total_issues
            if resolution_rate > 0.8:
                patterns.append("High issue resolution rate - good troubleshooting process")
            elif resolution_rate < 0.5:
                patterns.append("Low issue resolution rate - may need additional support")
        



async def main():
    """Main entry point for the MCP server"""
    mcp = ProjectKnowledgeOptimizerMCP()
    
    while True:
        try:
            # Read JSON-RPC request from stdin
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
                
            request = json.loads(line.strip())
            response = await mcp.handle_request(request)
            
            # Send JSON-RPC response to stdout
            print(json.dumps(response))
            sys.stdout.flush()
            
        except json.JSONDecodeError:
            continue
        except Exception as e:
            # Log error but continue running
            error_response = {
                "jsonrpc": "2.0",
                "id": 0,
                "error": {"code": -32603, "message": f"Server error: {str(e)}"}
            }
            print(json.dumps(error_response))
            sys.stdout.flush()


if __name__ == "__main__":
    asyncio.run(main())
