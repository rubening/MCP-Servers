#!/usr/bin/env python3

import asyncio
import json
import os
import sys
import shutil
import stat
from datetime import datetime
from typing import Any, Dict, List
import fnmatch

class FilesystemMCP:
    def __init__(self):
        self.allowed_directories = [
            os.path.expanduser("~"),
            "C:\\Users\\ruben\\Claude Tools",
            "C:\\temp",
            "C:\\Users\\ruben\\Desktop", 
            "C:\\Users\\ruben\\Documents",
            "D:\\",  # Areas - PARA ongoing responsibilities
            "E:\\",  # Active Projects - PARA current work
            "F:\\",  # Resources - Blue - PARA reference materials  
            "G:\\",  # Temporary backup - Staging & backup workflows
            "H:\\",  # Most Used Programs - PCIe 4.0 applications
            "I:\\",  # Archive - Black - PARA completed/historical
        ]
    
    def is_path_allowed(self, path):
        abs_path = os.path.abspath(path)
        for allowed in self.allowed_directories:
            abs_allowed = os.path.abspath(allowed)
            if abs_path.startswith(abs_allowed):
                return True
        return False
    
    def get_request_id(self, request):
        req_id = request.get("id")
        if req_id is None:
            return 0
        return req_id
    
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
                        "serverInfo": {"name": "filesystem-mcp", "version": "2.0.1"}
                    }
                }
            
            elif method == "tools/list":
                return {
                    "jsonrpc": "2.0", 
                    "id": request_id,
                    "result": {
                        "tools": [
                            {
                                "name": "list_directory",
                                "description": "List contents of a directory",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {"path": {"type": "string", "description": "Directory path to list"}},
                                    "required": ["path"]
                                }
                            },
                            {
                                "name": "read_file", 
                                "description": "Read contents of a file",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {"path": {"type": "string", "description": "File path to read"}},
                                    "required": ["path"]
                                }
                            },
                            {
                                "name": "read_multiple_files",
                                "description": "Read contents of multiple files at once",
                                "inputSchema": {
                                    "type": "object", 
                                    "properties": {"paths": {"type": "array", "items": {"type": "string"}, "description": "Array of file paths to read"}},
                                    "required": ["paths"]
                                }
                            },
                            {
                                "name": "write_file",
                                "description": "Write content to a file (creates new or overwrites existing)",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "path": {"type": "string", "description": "File path to write to"},
                                        "content": {"type": "string", "description": "Content to write to the file"}
                                    },
                                    "required": ["path", "content"]
                                }
                            },
                            {
                                "name": "edit_file",
                                "description": "Edit specific parts of a file without rewriting everything",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "path": {"type": "string", "description": "File path to edit"},
                                        "old_text": {"type": "string", "description": "Text to find and replace"},
                                        "new_text": {"type": "string", "description": "New text to replace with"}
                                    },
                                    "required": ["path", "old_text", "new_text"]
                                }
                            },
                            {
                                "name": "create_directory",
                                "description": "Create a new directory/folder",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {"path": {"type": "string", "description": "Directory path to create"}},
                                    "required": ["path"]
                                }
                            },
                            {
                                "name": "directory_tree",
                                "description": "Show directory structure as a tree",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "path": {"type": "string", "description": "Root directory to show tree for"},
                                        "max_depth": {"type": "integer", "description": "Maximum depth to show (default: 3)", "default": 3}
                                    },
                                    "required": ["path"]
                                }
                            },
                            {
                                "name": "move_file",
                                "description": "Move or rename a file/directory",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "source": {"type": "string", "description": "Current path of file/directory"},
                                        "destination": {"type": "string", "description": "New path for file/directory"}
                                    },
                                    "required": ["source", "destination"]
                                }
                            },
                            {
                                "name": "search_files",
                                "description": "Search for files by name pattern or content",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "directory": {"type": "string", "description": "Directory to search in"},
                                        "pattern": {"type": "string", "description": "File name pattern (supports wildcards like *.txt)"},
                                        "content": {"type": "string", "description": "Text to search for inside files (optional)"}
                                    },
                                    "required": ["directory", "pattern"]
                                }
                            },
                            {
                                "name": "get_file_info",
                                "description": "Get detailed information about a file or directory",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {"path": {"type": "string", "description": "Path to get information about"}},
                                    "required": ["path"]
                                }
                            },
                            {
                                "name": "list_allowed_directories",
                                "description": "List directories that this MCP server can access",
                                "inputSchema": {"type": "object", "properties": {}}
                            }
                        ]
                    }
                }
                
            elif method == "tools/call":
                params = request.get("params", {})
                tool_name = params.get("name", "")
                arguments = params.get("arguments", {})
                
                # Security check
                if tool_name != "list_allowed_directories":
                    path = arguments.get("path") or arguments.get("directory") or arguments.get("source")
                    if path and not self.is_path_allowed(path):
                        return {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "result": {"content": [{"type": "text", "text": f"Access denied: Path '{path}' is not in allowed directories"}]}
                        }
                
                # Route to tool functions
                if tool_name == "list_directory":
                    return await self.list_directory(request_id, arguments)
                elif tool_name == "read_file":
                    return await self.read_file(request_id, arguments)
                elif tool_name == "read_multiple_files":
                    return await self.read_multiple_files(request_id, arguments)
                elif tool_name == "write_file":
                    return await self.write_file(request_id, arguments)
                elif tool_name == "edit_file":
                    return await self.edit_file(request_id, arguments)
                elif tool_name == "create_directory":
                    return await self.create_directory(request_id, arguments)
                elif tool_name == "directory_tree":
                    return await self.directory_tree(request_id, arguments)
                elif tool_name == "move_file":
                    return await self.move_file(request_id, arguments)
                elif tool_name == "search_files":
                    return await self.search_files(request_id, arguments)
                elif tool_name == "get_file_info":
                    return await self.get_file_info(request_id, arguments)
                elif tool_name == "list_allowed_directories":
                    return await self.list_allowed_directories(request_id, arguments)
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
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
            }

    async def list_directory(self, request_id, arguments):
        path = arguments.get("path", ".")
        try:
            items = []
            for item in sorted(os.listdir(path)):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    items.append(f"[DIR] {item}/")
                else:
                    size = os.path.getsize(item_path)
                    items.append(f"[FILE] {item} ({size} bytes)")
            content = f"Contents of {path}:\n" + "\n".join(items)
        except Exception as e:
            content = f"Error listing directory: {str(e)}"
        
        return {
            "jsonrpc": "2.0",
            "id": request_id, 
            "result": {"content": [{"type": "text", "text": content}]}
        }

    async def read_file(self, request_id, arguments):
        path = arguments.get("path", "")
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            result_text = f"File: {path}\n\n{content}"
        except Exception as e:
            result_text = f"Error reading file: {str(e)}"
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": result_text}]}
        }

    async def read_multiple_files(self, request_id, arguments):
        paths = arguments.get("paths", [])
        results = []
        
        for path in paths:
            if not self.is_path_allowed(path):
                results.append(f"ERROR {path}: Access denied")
                continue
                
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                results.append(f"FILE {path}:\n{content}\n{'='*50}")
            except Exception as e:
                results.append(f"ERROR {path}: {str(e)}")
        
        result_text = f"Reading {len(paths)} files:\n\n" + "\n\n".join(results)
        
        return {
            "jsonrpc": "2.0", 
            "id": request_id,
            "result": {"content": [{"type": "text", "text": result_text}]}
        }

    async def write_file(self, request_id, arguments):
        path = arguments.get("path", "")
        content = arguments.get("content", "")
        
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            result_text = f"SUCCESS: Wrote {len(content)} characters to {path}"
        except Exception as e:
            result_text = f"ERROR writing file: {str(e)}"
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": result_text}]}
        }

    async def edit_file(self, request_id, arguments):
        path = arguments.get("path", "")
        old_text = arguments.get("old_text", "")
        new_text = arguments.get("new_text", "")
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if old_text in content:
                new_content = content.replace(old_text, new_text)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                result_text = f"SUCCESS: Replaced text in {path}"
            else:
                result_text = f"ERROR: Text not found in {path}"
                
        except Exception as e:
            result_text = f"ERROR editing file: {str(e)}"
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": result_text}]}
        }

    async def create_directory(self, request_id, arguments):
        path = arguments.get("path", "")
        
        try:
            os.makedirs(path, exist_ok=True)
            result_text = f"SUCCESS: Created directory {path}"
        except Exception as e:
            result_text = f"ERROR creating directory: {str(e)}"
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": result_text}]}
        }

    async def directory_tree(self, request_id, arguments):
        path = arguments.get("path", ".")
        max_depth = arguments.get("max_depth", 3)
        
        def build_tree(directory, prefix="", depth=0):
            if depth > max_depth:
                return []
            
            items = []
            try:
                entries = sorted(os.listdir(directory))
                for i, entry in enumerate(entries):
                    entry_path = os.path.join(directory, entry)
                    is_last = i == len(entries) - 1
                    
                    if os.path.isdir(entry_path):
                        connector = "|-- " if is_last else "+-- "
                        items.append(f"{prefix}{connector}[DIR] {entry}/")
                        
                        if depth < max_depth:
                            extension = "    " if is_last else "|   "
                            items.extend(build_tree(entry_path, prefix + extension, depth + 1))
                    else:
                        connector = "|-- " if is_last else "+-- "
                        size = os.path.getsize(entry_path)
                        items.append(f"{prefix}{connector}[FILE] {entry} ({size} bytes)")
                        
            except PermissionError:
                items.append(f"{prefix}ERROR: Permission denied")
            except Exception as e:
                items.append(f"{prefix}ERROR: {str(e)}")
            
            return items
        
        try:
            tree_lines = [f"[DIR] {os.path.basename(path) or path}"]
            tree_lines.extend(build_tree(path))
            result_text = "\n".join(tree_lines)
        except Exception as e:
            result_text = f"ERROR generating tree: {str(e)}"
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": result_text}]}
        }

    async def move_file(self, request_id, arguments):
        source = arguments.get("source", "")
        destination = arguments.get("destination", "")
        
        try:
            if not self.is_path_allowed(destination):
                result_text = f"ERROR: Access denied for destination {destination}"
            else:
                shutil.move(source, destination)
                result_text = f"SUCCESS: Moved {source} to {destination}"
        except Exception as e:
            result_text = f"ERROR moving file: {str(e)}"
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": result_text}]}
        }

    async def search_files(self, request_id, arguments):
        directory = arguments.get("directory", ".")
        pattern = arguments.get("pattern", "*")
        search_content = arguments.get("content", "")
        
        results = []
        
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if fnmatch.fnmatch(file, pattern):
                        file_path = os.path.join(root, file)
                        
                        if search_content:
                            try:
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                if search_content.lower() in content.lower():
                                    results.append(f"MATCH: {file_path} (contains '{search_content}')")
                            except:
                                pass
                        else:
                            results.append(f"FOUND: {file_path}")
            
            if results:
                result_text = f"Found {len(results)} files matching pattern '{pattern}':\n\n" + "\n".join(results)
            else:
                result_text = f"No files found matching pattern '{pattern}' in {directory}"
                
        except Exception as e:
            result_text = f"ERROR searching files: {str(e)}"
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": result_text}]}
        }

    async def get_file_info(self, request_id, arguments):
        path = arguments.get("path", "")
        
        try:
            stats = os.stat(path)
            is_dir = os.path.isdir(path)
            
            size_bytes = stats.st_size
            if size_bytes < 1024:
                size_str = f"{size_bytes} bytes"
            elif size_bytes < 1024 * 1024:
                size_str = f"{size_bytes / 1024:.1f} KB"
            else:
                size_str = f"{size_bytes / (1024 * 1024):.1f} MB"
            
            created = datetime.fromtimestamp(stats.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
            modified = datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            accessed = datetime.fromtimestamp(stats.st_atime).strftime("%Y-%m-%d %H:%M:%S")
            
            permissions = stat.filemode(stats.st_mode)
            
            result_text = f"""File Information: {path}

Type: {'Directory' if is_dir else 'File'}
Size: {size_str}
Permissions: {permissions}

Timestamps:
- Created: {created}
- Modified: {modified}  
- Accessed: {accessed}

Full path: {os.path.abspath(path)}"""

        except Exception as e:
            result_text = f"ERROR getting file info: {str(e)}"
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": result_text}]}
        }

    async def list_allowed_directories(self, request_id, arguments):
        result_text = "Allowed Directories:\n\n" + "\n".join([f"- {dir}" for dir in self.allowed_directories])
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": result_text}]}
        }

async def main():
    mcp = FilesystemMCP()
    
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
                
            request = json.loads(line.strip())
            response = await mcp.handle_request(request)
            
            print(json.dumps(response))
            sys.stdout.flush()
            
        except json.JSONDecodeError:
            continue
        except Exception as e:
            continue

if __name__ == "__main__":
    asyncio.run(main())
