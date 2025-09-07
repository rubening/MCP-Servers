#!/usr/bin/env python3
"""
Git MCP Server - Version Control Operations for Claude Desktop
Built on proven MCP architecture patterns from Ruben's AI tools ecosystem

This server provides secure Git operations through MCP protocol, enabling
version control foundation for advanced development projects.

Author: Claude & Ruben
Date: June 9, 2025
Version: 1.0.0
"""

import asyncio
import json
import logging
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
# Configure encoding for Windows
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')
logger = logging.getLogger(__name__)

class GitMCPServer:
    """Git MCP Server providing version control operations through MCP protocol."""
    
    def __init__(self):
        self.version = "1.0.0"
        self.server_name = "git-mcp"
        self.working_directory = None
        
        # Security: Commands that require special validation
        self.destructive_commands = {
            'reset_hard', 'force_push', 'delete_branch_force', 
            'clean_force', 'reset_commit'
        }
        
        # Initialize log directory
        log_dir = Path(r"C:\Users\ruben\Claude Tools\logs")
        log_dir.mkdir(exist_ok=True)
        
        # Set up file logging
        self.log_file = log_dir / "git_mcp.log"
        try:
            file_handler = logging.FileHandler(self.log_file)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            ))
            logger.addHandler(file_handler)
        except Exception as e:
            # If file logging fails, continue without it
            print(f"Warning: Could not set up file logging: {e}", file=sys.stderr)
        
        logger.info(f"Git MCP Server v{self.version} initialized")

    async def run_git_command(self, args: List[str], cwd: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute git command safely with comprehensive error handling.
        
        Args:
            args: Git command arguments (e.g., ['status', '--porcelain'])
            cwd: Working directory for command execution
            
        Returns:
            Dict with success status, output, error, and metadata
        """
        # Use provided cwd or default working directory
        work_dir = cwd or self.working_directory or os.getcwd()
        
        # Try multiple Git executable locations
        git_locations = [
            'git',  # Try PATH first
            'C:\\Program Files\\Git\\bin\\git.exe',  # Standard Windows location
            'C:\\Program Files (x86)\\Git\\bin\\git.exe',  # 32-bit location
        ]
        
        git_exe = None
        for location in git_locations:
            try:
                subprocess.run([location, '--version'], capture_output=True, check=True, timeout=5)
                git_exe = location
                break
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                continue
        
        if not git_exe:
            return {
                'success': False,
                'error': 'Git is not installed or not available in any expected location',
                'output': '',
                'command': f'git {" ".join(args)}',
                'working_directory': work_dir
            }
        
        # Build full command
        full_command = [git_exe] + args
        command_str = ' '.join(full_command)
        
        # Log command execution
        logger.info(f"Executing: {command_str} in {work_dir}")
        
        start_time = datetime.now()
        
        try:
            # Execute git command
            process = subprocess.run(
                full_command,
                cwd=work_dir,
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout
            )
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            result = {
                'success': process.returncode == 0,
                'output': process.stdout.strip(),
                'error': process.stderr.strip(),
                'return_code': process.returncode,
                'command': command_str,
                'working_directory': work_dir,
                'duration_seconds': duration,
                'timestamp': end_time.isoformat()
            }
            
            # Log result
            if result['success']:
                logger.info(f"Command succeeded in {duration:.2f}s: {command_str}")
            else:
                logger.warning(f"Command failed in {duration:.2f}s: {command_str} - {result['error']}")
            
            return result
            
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out: {command_str}")
            return {
                'success': False,
                'error': f'Command timed out after 30 seconds',
                'output': '',
                'command': command_str,
                'working_directory': work_dir
            }
        except Exception as e:
            logger.error(f"Command execution error: {command_str} - {str(e)}")
            return {
                'success': False,
                'error': f'Execution error: {str(e)}',
                'output': '',
                'command': command_str,
                'working_directory': work_dir
            }

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP requests with proper JSON-RPC 2.0 protocol."""
        try:
            method = request.get('method')
            params = request.get('params', {})
            request_id = request.get('id')
            
            logger.info(f"Handling request: {method}")
            
            if method == 'initialize':
                return await self.handle_initialize(request_id, params)
            elif method == 'tools/list':
                return await self.handle_tools_list(request_id)
            elif method == 'tools/call':
                return await self.handle_tool_call(request_id, params)
            elif method == 'notifications/initialized':
                return None  # No response needed for notification
            else:
                return {
                    'jsonrpc': '2.0',
                    'id': request_id,
                    'error': {
                        'code': -32601,
                        'message': f'Method not found: {method}'
                    }
                }
        except Exception as e:
            logger.error(f"Request handling error: {str(e)}")
            return {
                'jsonrpc': '2.0',
                'id': request.get('id'),
                'error': {
                    'code': -32603,
                    'message': f'Internal error: {str(e)}'
                }
            }

    async def handle_initialize(self, request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP initialize request."""
        return {
            'jsonrpc': '2.0',
            'id': request_id,
            'result': {
                'protocolVersion': '2024-11-05',
                'capabilities': {
                    'tools': {}
                },
                'serverInfo': {
                    'name': self.server_name,
                    'version': self.version
                }
            }
        }

    async def handle_tools_list(self, request_id: Any) -> Dict[str, Any]:
        """Return list of available Git tools."""
        tools = [
            {
                'name': 'git_status',
                'description': 'Check the status of a Git repository, showing modified, staged, and untracked files',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'repository_path': {
                            'type': 'string',
                            'description': 'Path to the Git repository (optional, uses current working directory if not specified)'
                        }
                    }
                }
            },
            {
                'name': 'git_init',
                'description': 'Initialize a new Git repository in the specified directory',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'repository_path': {
                            'type': 'string',
                            'description': 'Path where to initialize the Git repository'
                        }
                    },
                    'required': ['repository_path']
                }
            },
            {
                'name': 'git_add',
                'description': 'Stage files for commit in the Git repository',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'file_paths': {
                            'type': 'array',
                            'items': {'type': 'string'},
                            'description': 'List of file paths to stage. Use ["."] to stage all changes'
                        },
                        'repository_path': {
                            'type': 'string',
                            'description': 'Path to the Git repository (optional, uses current working directory if not specified)'
                        }
                    },
                    'required': ['file_paths']
                }
            },
            {
                'name': 'git_commit',
                'description': 'Create a new commit with staged changes',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'message': {
                            'type': 'string',
                            'description': 'Commit message describing the changes'
                        },
                        'repository_path': {
                            'type': 'string',
                            'description': 'Path to the Git repository (optional, uses current working directory if not specified)'
                        }
                    },
                    'required': ['message']
                }
            },
            {
                'name': 'git_log',
                'description': 'View commit history with optional filtering',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'max_count': {
                            'type': 'integer',
                            'description': 'Maximum number of commits to show (default: 10)',
                            'default': 10
                        },
                        'oneline': {
                            'type': 'boolean',
                            'description': 'Show each commit on a single line (default: true)',
                            'default': True
                        },
                        'repository_path': {
                            'type': 'string',
                            'description': 'Path to the Git repository (optional, uses current working directory if not specified)'
                        }
                    }
                }
            },
            {
                'name': 'git_diff',
                'description': 'Show differences between working directory, staged changes, or commits',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'file_path': {
                            'type': 'string',
                            'description': 'Specific file to show diff for (optional, shows all changes if not specified)'
                        },
                        'staged': {
                            'type': 'boolean',
                            'description': 'Show differences of staged changes (default: false)',
                            'default': False
                        },
                        'repository_path': {
                            'type': 'string',
                            'description': 'Path to the Git repository (optional, uses current working directory if not specified)'
                        }
                    }
                }
            },
            {
                'name': 'git_branch',
                'description': 'List, create, or switch branches',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'action': {
                            'type': 'string',
                            'enum': ['list', 'create', 'switch'],
                            'description': 'Action to perform: list (show all branches), create (new branch), switch (change branch)'
                        },
                        'branch_name': {
                            'type': 'string',
                            'description': 'Branch name (required for create and switch actions)'
                        },
                        'repository_path': {
                            'type': 'string',
                            'description': 'Path to the Git repository (optional, uses current working directory if not specified)'
                        }
                    },
                    'required': ['action']
                }
            },
            {
                'name': 'git_remote',
                'description': 'Manage remote repositories',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'action': {
                            'type': 'string',
                            'enum': ['list', 'add', 'remove'],
                            'description': 'Action to perform with remotes'
                        },
                        'remote_name': {
                            'type': 'string',
                            'description': 'Name of the remote (required for add and remove)'
                        },
                        'remote_url': {
                            'type': 'string',
                            'description': 'URL of the remote repository (required for add)'
                        },
                        'repository_path': {
                            'type': 'string',
                            'description': 'Path to the Git repository (optional, uses current working directory if not specified)'
                        }
                    },
                    'required': ['action']
                }
            },
            {
                'name': 'git_push',
                'description': 'Push commits to remote repository',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'remote_name': {
                            'type': 'string',
                            'description': 'Name of the remote to push to (default: origin)',
                            'default': 'origin'
                        },
                        'branch_name': {
                            'type': 'string',
                            'description': 'Branch to push (optional, uses current branch if not specified)'
                        },
                        'force': {
                            'type': 'boolean',
                            'description': 'Force push (DANGEROUS - use with caution)',
                            'default': False
                        },
                        'repository_path': {
                            'type': 'string',
                            'description': 'Path to the Git repository (optional, uses current working directory if not specified)'
                        }
                    }
                }
            },
            {
                'name': 'git_pull',
                'description': 'Pull changes from remote repository',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'remote_name': {
                            'type': 'string',
                            'description': 'Name of the remote to pull from (default: origin)',
                            'default': 'origin'
                        },
                        'branch_name': {
                            'type': 'string',
                            'description': 'Branch to pull (optional, uses current branch if not specified)'
                        },
                        'repository_path': {
                            'type': 'string',
                            'description': 'Path to the Git repository (optional, uses current working directory if not specified)'
                        }
                    }
                }
            },
            {
                'name': 'set_working_directory',
                'description': 'Set the default working directory for Git operations',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'directory_path': {
                            'type': 'string',
                            'description': 'Path to set as the working directory'
                        }
                    },
                    'required': ['directory_path']
                }
            }
        ]
        
        return {
            'jsonrpc': '2.0',
            'id': request_id,
            'result': {
                'tools': tools
            }
        }

    async def handle_tool_call(self, request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool execution requests."""
        tool_name = params.get('name')
        arguments = params.get('arguments', {})
        
        logger.info(f"Executing tool: {tool_name} with args: {arguments}")
        
        try:
            if tool_name == 'git_status':
                result = await self.git_status(arguments)
            elif tool_name == 'git_init':
                result = await self.git_init(arguments)
            elif tool_name == 'git_add':
                result = await self.git_add(arguments)
            elif tool_name == 'git_commit':
                result = await self.git_commit(arguments)
            elif tool_name == 'git_log':
                result = await self.git_log(arguments)
            elif tool_name == 'git_diff':
                result = await self.git_diff(arguments)
            elif tool_name == 'git_branch':
                result = await self.git_branch(arguments)
            elif tool_name == 'git_remote':
                result = await self.git_remote(arguments)
            elif tool_name == 'git_push':
                result = await self.git_push(arguments)
            elif tool_name == 'git_pull':
                result = await self.git_pull(arguments)
            elif tool_name == 'set_working_directory':
                result = await self.set_working_directory(arguments)
            else:
                result = {
                    'success': False,
                    'error': f'Unknown tool: {tool_name}'
                }
            
            return {
                'jsonrpc': '2.0',
                'id': request_id,
                'result': {
                    'content': [
                        {
                            'type': 'text',
                            'text': json.dumps(result, indent=2)
                        }
                    ]
                }
            }
            
        except Exception as e:
            logger.error(f"Tool execution error: {tool_name} - {str(e)}")
            return {
                'jsonrpc': '2.0',
                'id': request_id,
                'error': {
                    'code': -32603,
                    'message': f'Tool execution failed: {str(e)}'
                }
            }

    # Git Tool Implementations
    
    async def git_status(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get repository status."""
        repo_path = args.get('repository_path')
        result = await self.run_git_command(['status', '--porcelain'], cwd=repo_path)
        
        if result['success']:
            # Parse status output for better readability
            status_lines = result['output'].split('\n') if result['output'] else []
            changes = {
                'modified': [],
                'added': [],
                'deleted': [],
                'untracked': [],
                'renamed': []
            }
            
            for line in status_lines:
                if len(line) >= 3:
                    status_code = line[:2]
                    file_path = line[3:]
                    
                    if status_code.startswith('M'):
                        changes['modified'].append(file_path)
                    elif status_code.startswith('A'):
                        changes['added'].append(file_path)
                    elif status_code.startswith('D'):
                        changes['deleted'].append(file_path)
                    elif status_code.startswith('??'):
                        changes['untracked'].append(file_path)
                    elif status_code.startswith('R'):
                        changes['renamed'].append(file_path)
            
            result['parsed_status'] = changes
            result['has_changes'] = any(changes.values())
        
        return result

    async def git_init(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize a new Git repository."""
        repo_path = args.get('repository_path')
        if not repo_path:
            return {'success': False, 'error': 'repository_path is required'}
        
        # Ensure directory exists
        Path(repo_path).mkdir(parents=True, exist_ok=True)
        
        return await self.run_git_command(['init'], cwd=repo_path)

    async def git_add(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Stage files for commit."""
        file_paths = args.get('file_paths', [])
        repo_path = args.get('repository_path')
        
        if not file_paths:
            return {'success': False, 'error': 'file_paths is required'}
        
        command_args = ['add'] + file_paths
        return await self.run_git_command(command_args, cwd=repo_path)

    async def git_commit(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new commit."""
        message = args.get('message')
        repo_path = args.get('repository_path')
        
        if not message:
            return {'success': False, 'error': 'message is required'}
        
        return await self.run_git_command(['commit', '-m', message], cwd=repo_path)

    async def git_log(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """View commit history."""
        max_count = args.get('max_count', 10)
        oneline = args.get('oneline', True)
        repo_path = args.get('repository_path')
        
        command_args = ['log', f'--max-count={max_count}']
        if oneline:
            command_args.append('--oneline')
        
        return await self.run_git_command(command_args, cwd=repo_path)

    async def git_diff(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Show differences."""
        file_path = args.get('file_path')
        staged = args.get('staged', False)
        repo_path = args.get('repository_path')
        
        command_args = ['diff']
        if staged:
            command_args.append('--staged')
        if file_path:
            command_args.append(file_path)
        
        return await self.run_git_command(command_args, cwd=repo_path)

    async def git_branch(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Manage branches."""
        action = args.get('action')
        branch_name = args.get('branch_name')
        repo_path = args.get('repository_path')
        
        if action == 'list':
            return await self.run_git_command(['branch', '-a'], cwd=repo_path)
        elif action == 'create':
            if not branch_name:
                return {'success': False, 'error': 'branch_name is required for create action'}
            return await self.run_git_command(['branch', branch_name], cwd=repo_path)
        elif action == 'switch':
            if not branch_name:
                return {'success': False, 'error': 'branch_name is required for switch action'}
            return await self.run_git_command(['checkout', branch_name], cwd=repo_path)
        else:
            return {'success': False, 'error': f'Unknown action: {action}'}

    async def git_remote(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Manage remote repositories."""
        action = args.get('action')
        remote_name = args.get('remote_name')
        remote_url = args.get('remote_url')
        repo_path = args.get('repository_path')
        
        if action == 'list':
            return await self.run_git_command(['remote', '-v'], cwd=repo_path)
        elif action == 'add':
            if not remote_name or not remote_url:
                return {'success': False, 'error': 'remote_name and remote_url are required for add action'}
            return await self.run_git_command(['remote', 'add', remote_name, remote_url], cwd=repo_path)
        elif action == 'remove':
            if not remote_name:
                return {'success': False, 'error': 'remote_name is required for remove action'}
            return await self.run_git_command(['remote', 'remove', remote_name], cwd=repo_path)
        else:
            return {'success': False, 'error': f'Unknown action: {action}'}

    async def git_push(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Push commits to remote."""
        remote_name = args.get('remote_name', 'origin')
        branch_name = args.get('branch_name')
        force = args.get('force', False)
        repo_path = args.get('repository_path')
        
        command_args = ['push']
        if force:
            # Log force push for security audit
            logger.warning(f"FORCE PUSH attempted: {remote_name}/{branch_name}")
            command_args.append('--force')
        
        command_args.append(remote_name)
        if branch_name:
            command_args.append(branch_name)
        
        return await self.run_git_command(command_args, cwd=repo_path)

    async def git_pull(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Pull changes from remote."""
        remote_name = args.get('remote_name', 'origin')
        branch_name = args.get('branch_name')
        repo_path = args.get('repository_path')
        
        command_args = ['pull', remote_name]
        if branch_name:
            command_args.append(branch_name)
        
        return await self.run_git_command(command_args, cwd=repo_path)

    async def set_working_directory(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Set the default working directory."""
        directory_path = args.get('directory_path')
        
        if not directory_path:
            return {'success': False, 'error': 'directory_path is required'}
        
        if not os.path.exists(directory_path):
            return {'success': False, 'error': f'Directory does not exist: {directory_path}'}
        
        if not os.path.isdir(directory_path):
            return {'success': False, 'error': f'Path is not a directory: {directory_path}'}
        
        self.working_directory = directory_path
        logger.info(f"Working directory set to: {directory_path}")
        
        return {
            'success': True,
            'message': f'Working directory set to: {directory_path}',
            'working_directory': directory_path
        }

async def main():
    """Main server loop for Git MCP Server."""
    server = GitMCPServer()
    
    # Main communication loop using async stdin reading (like working servers)
    while True:
        try:
            # Read request from stdin asynchronously
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
            
            request = json.loads(line.strip())
            response = await server.handle_request(request)
            
            if response:
                print(json.dumps(response))
                sys.stdout.flush()
                
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            error_response = {
                'jsonrpc': '2.0',
                'id': None,
                'error': {
                    'code': -32700,
                    'message': 'Parse error'
                }
            }
            print(json.dumps(error_response))
            sys.stdout.flush()
        except KeyboardInterrupt:
            logger.info("Server shutdown requested")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            # Continue running instead of breaking on errors
            continue

if __name__ == "__main__":
    asyncio.run(main())
