# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a collection of Python-based MCP (Model Context Protocol) servers designed for integration with Claude Desktop. Each server provides specialized tools and capabilities for different domains like analytics, version control, file operations, AI reasoning, and business automation.

## Architecture & Code Patterns

### MCP Server Structure
All servers follow a consistent JSON-RPC 2.0 pattern:

- **Main server class** implementing `handle_request()` method
- **Async main loop** reading from stdin using `asyncio.get_event_loop().run_in_executor()`
- **Tool definitions** with proper JSON-RPC method routing
- **Error handling** with proper JSON-RPC error responses
- **Logging setup** with UTF-8 encoding configuration for Windows

### Common Server Types
1. **Core servers** (root directory): `git_mcp.py`, `filesystem_mcp.py`, `execute_command_mcp.py`
2. **Analytics servers**: `duckdb_analytics_fixed.py`, DuckDB integration for data processing
3. **AI servers**: DeepSeek integration for reasoning capabilities
4. **Business servers**: Lead qualification, project management, knowledge intelligence
5. **Integration servers**: Google services (Ads, Calendar, Sheets), YouTube, Chroma

### File Naming Conventions
- Main servers: `[service]_mcp.py`
- Fixed/updated versions: `[service]_mcp_fixed.py` or `[service]_fixed.py`
- Test files: `test_[service].py`
- Subdirectories contain organized server implementations

## Development Commands

### Running Individual Servers
```bash
# Run any MCP server directly for testing
py [server_name].py

# Example: Test DeepSeek integration
py test_deepseek.py

# Run specific servers
py git_mcp.py
py filesystem_mcp.py
py duckdb_analytics_fixed.py
```

### Python Environment
- **Python Version**: 3.13.3
- **Core Dependencies**: `requests>=2.31.0`, `asyncio`, `json`, `sqlite3`
- **Database**: DuckDB for analytics, SQLite for local storage
- **Protocol**: JSON-RPC 2.0 over stdin/stdout

### Testing Servers
Use the test pattern from `test_deepseek.py`:
```python
# Test initialize, tools/list, and tools/call methods
async def test_server():
    server = YourMCPServer()
    
    # Test initialize request
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {"protocolVersion": "2024-11-05", "capabilities": {}}
    }
    response = await server.handle_request(init_request)
    
    # Test tools list
    tools_request = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
    response = await server.handle_request(tools_request)
    
    # Test tool call
    tool_request = {
        "jsonrpc": "2.0", "id": 3, "method": "tools/call",
        "params": {"name": "tool_name", "arguments": {}}
    }
    response = await server.handle_request(tool_request)

asyncio.run(test_server())
```

## Key Server Capabilities

### Core Infrastructure
- **Git MCP** (`git_mcp.py`): Version control operations with security validation
- **Filesystem MCP** (`filesystem_mcp.py`): File operations with path restrictions
- **Execute Command** (`execute_command_mcp.py`): Safe command execution with timeout

### Data & Analytics
- **DuckDB Analytics** (`duckdb_analytics_fixed.py`): High-performance SQL analytics
- **Personal Knowledge Intelligence**: Conversation insight capture and analysis

### AI Integration
- **DeepSeek MCP**: Advanced reasoning capabilities with multiple variants
- **Project Instructions Generator**: Automated documentation and instruction creation

### Business Automation
- **Lead Qualification MCP**: CRM integration with scoring algorithms
- **Project Management MCP**: Task tracking with milestone management
- **Google Services**: Calendar, Sheets, and Ads integration

## Database Integration

### DuckDB Analytics Pattern
```python
# Standard DuckDB setup for analytics servers
import duckdb

class AnalyticsServer:
    def __init__(self, db_path="analytics.db"):
        self.db = duckdb.connect(db_path)
        self.setup_database()
    
    def setup_database(self):
        # Create schemas and tables
        self.db.execute("CREATE SCHEMA IF NOT EXISTS analytics")
```

### SQLite Pattern for Local Storage
```python
# Standard SQLite setup for local data
import sqlite3

class LocalServer:
    def __init__(self, db_path="local.db"):
        self.db = sqlite3.connect(db_path)
        self.setup_database()
```

## Security Considerations

### Path Restrictions (Filesystem MCP)
Filesystem operations are restricted to allowed directories:
- User home directory
- `C:\Users\ruben\Claude Tools`
- `C:\temp`
- Drive letters D-I for organized storage (PARA method)

### Command Validation
- Destructive Git operations require special validation
- Execute command has timeout and safety checks
- All servers validate JSON-RPC requests properly

## Integration Patterns

### Claude Desktop Configuration
Add servers to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "server-name": {
      "command": "py",
      "args": ["C:\\path\\to\\server.py", "--optional-args"]
    }
  }
}
```

### Multi-Server Workflows
Servers are designed to work together:
1. **Data flow**: Filesystem → DuckDB Analytics → Knowledge Intelligence
2. **Development flow**: Git → Project Management → Execute Command
3. **Business flow**: Lead Qualification → Google Services → Analytics

## Error Handling Pattern
All servers follow consistent error handling:
```python
try:
    # Server operation
    return {"jsonrpc": "2.0", "id": request_id, "result": result}
except Exception as e:
    return {
        "jsonrpc": "2.0", "id": request_id,
        "error": {"code": -32000, "message": str(e)}
    }
```

## Performance Considerations

- **Async operations**: All servers use asyncio for non-blocking operations
- **Database connections**: Persistent connections with proper cleanup
- **Memory management**: Streaming large datasets when possible
- **Timeout handling**: Commands and operations have appropriate timeouts