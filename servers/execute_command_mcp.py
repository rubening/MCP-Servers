#!/usr/bin/env python3

import asyncio
import json
import logging
import os
import sys
import subprocess
import platform
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configure logging
log_dir = Path.home() / "Claude Tools" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "execute_command_mcp.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("execute_command_mcp")

class ExecuteCommandServer:
    def __init__(self):
        self.name = "execute-command-mcp"
        self.version = "1.0.1"
        
        # Security settings
        self.dangerous_commands = {
            'rm', 'del', 'rmdir', 'rd', 'format', 'fdisk', 'mkfs',
            'sudo rm', 'sudo del', 'shutdown', 'restart', 'reboot',
            'halt', 'poweroff', 'init 0', 'init 6', 'systemctl poweroff',
            'systemctl reboot', 'reg delete', 'reg add', 'diskpart'
        }
        
        # Get system info
        self.system = platform.system()
        self.is_windows = self.system == "Windows"
        self.shell = "powershell" if self.is_windows else "/bin/bash"
        
        logger.info(f"Execute Command MCP Server initialized on {self.system}")

    def get_request_id(self, request):
        req_id = request.get("id")
        if req_id is None:
            return 0
        return req_id

    def is_dangerous_command(self, command: str) -> bool:
        command_lower = command.lower().strip()
        
        for dangerous in self.dangerous_commands:
            if dangerous in command_lower:
                return True
                
        destructive_patterns = [
            'rm -rf', 'del /s', 'rmdir /s', 'format c:', '> /dev/null',
            'dd if=', 'mkfs.', '| rm', '&& rm', '; rm', 'rm *', 'del *'
        ]
        
        for pattern in destructive_patterns:
            if pattern in command_lower:
                return True
                
        return False

    async def execute_command(self, 
                            command: str, 
                            working_directory: Optional[str] = None,
                            timeout: int = 30,
                            shell_type: Optional[str] = None) -> Dict[str, Any]:
        start_time = datetime.now()
        
        if not command or not command.strip():
            return {
                "success": False,
                "error": "Empty command provided",
                "exit_code": -1,
                "stdout": "",
                "stderr": "Command cannot be empty",
                "execution_time": 0,
                "timestamp": start_time.isoformat()
            }
        
        logger.info(f"Executing command: {command}")
        
        if self.is_dangerous_command(command):
            logger.warning(f"Potentially dangerous command blocked: {command}")
            return {
                "success": False,
                "error": "Command blocked for security reasons",
                "exit_code": -1,
                "stdout": "",
                "stderr": f"Command '{command}' contains potentially dangerous operations and was blocked",
                "execution_time": 0,
                "timestamp": start_time.isoformat(),
                "security_warning": True
            }
        
        try:
            if shell_type:
                if shell_type.lower() == "powershell":
                    shell_cmd = ["powershell", "-Command", command]
                elif shell_type.lower() == "cmd":
                    shell_cmd = ["cmd", "/c", command]
                elif shell_type.lower() == "bash":
                    shell_cmd = ["bash", "-c", command]
                else:
                    shell_cmd = [shell_type, "-c", command]
            else:
                if self.is_windows:
                    shell_cmd = ["powershell", "-Command", command]
                else:
                    shell_cmd = ["bash", "-c", command]
            
            cwd = None
            if working_directory:
                cwd_path = Path(working_directory)
                if cwd_path.exists() and cwd_path.is_dir():
                    cwd = str(cwd_path.resolve())
                else:
                    return {
                        "success": False,
                        "error": f"Working directory does not exist: {working_directory}",
                        "exit_code": -1,
                        "stdout": "",
                        "stderr": f"Directory not found: {working_directory}",
                        "execution_time": 0,
                        "timestamp": start_time.isoformat()
                    }
            
            logger.info(f"Running: {' '.join(shell_cmd)}")
            
            process = await asyncio.create_subprocess_exec(
                *shell_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), 
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                end_time = datetime.now()
                execution_time = (end_time - start_time).total_seconds()
                
                logger.error(f"Command timed out after {timeout}s: {command}")
                return {
                    "success": False,
                    "error": f"Command timed out after {timeout} seconds",
                    "exit_code": -1,
                    "stdout": "",
                    "stderr": f"Command execution timed out after {timeout} seconds",
                    "execution_time": execution_time,
                    "timestamp": start_time.isoformat()
                }
            
            exit_code = process.returncode
            stdout_text = stdout.decode('utf-8', errors='replace').strip()
            stderr_text = stderr.decode('utf-8', errors='replace').strip()
            
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            logger.info(f"Command completed with exit code: {exit_code}")
            
            return {
                "success": exit_code == 0,
                "exit_code": exit_code,
                "stdout": stdout_text,
                "stderr": stderr_text,
                "execution_time": execution_time,
                "timestamp": start_time.isoformat(),
                "command": command,
                "working_directory": cwd,
                "shell": ' '.join(shell_cmd[:2]) if len(shell_cmd) >= 2 else shell_cmd[0]
            }
            
        except Exception as e:
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            logger.error(f"Error executing command: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "exit_code": -1,
                "stdout": "",
                "stderr": f"Internal error: {str(e)}",
                "execution_time": execution_time,
                "timestamp": start_time.isoformat()
            }

    async def get_system_info(self) -> Dict[str, Any]:
        try:
            info = {
                "system": platform.system(),
                "platform": platform.platform(),
                "architecture": platform.architecture(),
                "processor": platform.processor(),
                "python_version": platform.python_version(),
                "hostname": platform.node(),
                "default_shell": self.shell,
                "is_windows": self.is_windows
            }
            
            if self.is_windows:
                info["windows_version"] = platform.win32_ver()
                
                shells = {}
                try:
                    result = await self.execute_command("powershell -Command 'Get-Host | Select-Object Version'", timeout=5)
                    shells["powershell"] = "available" if result["success"] else "not available"
                except:
                    shells["powershell"] = "unknown"
                
                try:
                    result = await self.execute_command("cmd /c ver", timeout=5)
                    shells["cmd"] = "available" if result["success"] else "not available"
                except:
                    shells["cmd"] = "unknown"
                
                info["available_shells"] = shells
            else:
                info["unix_name"] = platform.uname()
                shells = {}
                for shell in ["/bin/bash", "/bin/sh", "/bin/zsh"]:
                    shells[shell] = "available" if Path(shell).exists() else "not available"
                info["available_shells"] = shells
            
            return info
            
        except Exception as e:
            logger.error(f"Error getting system info: {str(e)}")
            return {"error": str(e)}

    async def list_dangerous_commands(self) -> List[str]:
        return list(self.dangerous_commands)

    async def handle_request(self, request):
        method = request.get("method", "")
        request_id = self.get_request_id(request)
        
        try:
            if method == "initialize":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": self.name, "version": self.version}
                    }
                }
            
            elif method == "tools/list":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "tools": [
                            {
                                "name": "execute_command",
                                "description": "Execute shell commands with security controls and detailed output",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "command": {"type": "string", "description": "The shell command to execute"},
                                        "working_directory": {"type": "string", "description": "Directory to run the command in (optional)"},
                                        "timeout": {"type": "integer", "description": "Timeout in seconds (default: 30)", "default": 30},
                                        "shell_type": {"type": "string", "description": "Shell to use: powershell, cmd, bash (optional)", "enum": ["powershell", "cmd", "bash"]}
                                    },
                                    "required": ["command"]
                                }
                            },
                            {
                                "name": "get_system_info",
                                "description": "Get detailed system information and available capabilities",
                                "inputSchema": {"type": "object", "properties": {}}
                            },
                            {
                                "name": "list_dangerous_commands",
                                "description": "List commands that are blocked for security reasons",
                                "inputSchema": {"type": "object", "properties": {}}
                            }
                        ]
                    }
                }
            
            elif method == "tools/call":
                params = request.get("params", {})
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                if tool_name == "execute_command":
                    result = await self.execute_command(
                        command=arguments.get("command"),
                        working_directory=arguments.get("working_directory"),
                        timeout=arguments.get("timeout", 30),
                        shell_type=arguments.get("shell_type")
                    )
                    
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
                    }
                
                elif tool_name == "get_system_info":
                    result = await self.get_system_info()
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
                    }
                
                elif tool_name == "list_dangerous_commands":
                    result = await self.list_dangerous_commands()
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {"content": [{"type": "text", "text": json.dumps({"blocked_commands": result}, indent=2)}]}
                    }
                
                else:
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"}
                    }
            
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": f"Method not found: {method}"}
                }
        
        except Exception as e:
            logger.error(f"Error handling request: {str(e)}")
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
            }

async def main():
    logger.info("Starting Execute Command MCP Server...")
    server = ExecuteCommandServer()
    
    try:
        while True:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
            
            try:
                request = json.loads(line.strip())
                response = await server.handle_request(request)
                print(json.dumps(response), flush=True)
                
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON request: {e}")
                error_response = {
                    "jsonrpc": "2.0",
                    "id": 0,
                    "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
                }
                print(json.dumps(error_response), flush=True)
            
            except Exception as e:
                logger.error(f"Error processing request: {e}")
                error_response = {
                    "jsonrpc": "2.0",
                    "id": 0,
                    "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
                }
                print(json.dumps(error_response), flush=True)
    
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
    finally:
        logger.info("Execute Command MCP Server shutdown")

if __name__ == "__main__":
    asyncio.run(main())
