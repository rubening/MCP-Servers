# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Architecture

This is a comprehensive MCP (Model Context Protocol) server repository organized by functional categories. The repository manages a complete ecosystem of specialized servers that integrate with Claude Desktop to provide domain-specific capabilities.

### Directory Structure

**Servers are organized by functional categories:**
- `core-infrastructure/` - Essential system operations (filesystem, git, command execution)
- `external-services/` - Third-party integrations (GitHub, ClickUp, Google Drive, Playwright)
- `analytics-intelligence/` - Data analysis and knowledge management tools
- `ai-reasoning/` - AI-powered analysis and reasoning capabilities
- `business-tools/` - Business process automation and workflow management
- `tony-ramos-law/` - Client-specific specialized tools
- `experimental/` - Development and testing servers
- `archived/` - Deprecated servers maintained for reference

**The `servers/` directory** contains active Python MCP servers and already has its own CLAUDE.md for server-specific guidance.

### Key Server Types

**Core Infrastructure Servers** (`core-infrastructure/`, `servers/`):
- Filesystem operations with security restrictions
- Git version control with validation
- Safe command execution with timeouts
- YouTube video processing and management

**Analytics & Intelligence** (`analytics-intelligence/`, `servers/`):
- DuckDB for high-performance SQL analytics
- Personal knowledge intelligence with conversation capture
- Chroma vector database for secure data storage
- E5 marketing research capabilities

**Business Automation** (`business-tools/`):
- Lead qualification with CRM integration
- Project management with milestone tracking
- Project instruction generation
- MCP project optimizer for codebase analysis

## Development Commands

### Python Servers
```bash
# Test individual MCP servers
cd servers/
py [server_name].py

# Run server tests
py test_deepseek.py

# Install Python dependencies
pip install -r requirements.txt
```

### Node.js Servers
```bash
# For Node.js-based servers (e.g., web-search)
cd external-services/web-search-mcp-server/
npm install
npm start
```

### Configuration Generation
```bash
# Generate Claude Desktop configurations
cd scripts/
py generate_config.py
```

### Testing MCP Server Integration
All Python MCP servers follow the JSON-RPC 2.0 pattern with these standard methods:
- `initialize` - Server initialization with protocol version
- `tools/list` - List available tools/capabilities  
- `tools/call` - Execute specific tool with parameters

## Development Workflow

### Experimental Server Promotion Process
1. **Development**: Create in `experimental/` directory
2. **Testing**: Comprehensive test suites with JSON-RPC validation
3. **Documentation**: Complete README and API documentation
4. **Review**: Code review and performance validation
5. **Promotion**: Move to appropriate category directory
6. **Integration**: Update configurations and deploy

### Configuration Management
- Configuration templates in `configs/`
- Environment-specific configs: `claude_desktop_config_TEST.json`
- Server paths and environment variables managed centrally
- API keys stored in environment variables (never committed)

## Security & Best Practices

### Security Restrictions
**Filesystem servers** restrict operations to:
- User home directory
- `C:\Users\ruben\Claude Tools`
- `C:\temp`
- Drive letters D-I (PARA organization method)

**Git operations** require validation for destructive commands
**Command execution** has timeout and safety checks

### API Key Management
- Environment variables for all sensitive data
- Regular key rotation procedures
- Never commit credentials to version control
- Monitor access and usage patterns

## Integration Architecture

### Multi-Server Workflows
Servers are designed for coordinated operation:
1. **Data Pipeline**: Filesystem → DuckDB Analytics → Knowledge Intelligence
2. **Development Flow**: Git → Project Management → Execute Command  
3. **Business Flow**: Lead Qualification → Google Services → Analytics

### Claude Desktop Integration
Add servers to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "server-name": {
      "command": "py",
      "args": ["C:\\full\\path\\to\\server.py"]
    }
  }
}
```

## Performance Considerations

### Async Architecture
- All servers use asyncio for non-blocking operations
- JSON-RPC 2.0 over stdin/stdout communication
- Persistent database connections with proper cleanup
- Streaming for large dataset operations

### Database Integration Patterns
- **DuckDB**: High-performance analytics and OLAP operations
- **SQLite**: Local storage for simple data persistence
- **Chroma**: Vector database for semantic search and AI operations

## Backup & Recovery

### Automated Systems
- **Nightly**: Full repository backup to OneDrive
- **Weekly**: Complete system snapshots including databases
- **Monthly**: Archive cleanup and version management

### Recovery Procedures
1. Restore code from GitHub main branch
2. Restore databases from backup snapshots
3. Reconfigure environment variables and API keys
4. Verify server connectivity and functionality

## Error Handling Standards

All MCP servers implement consistent error patterns:
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

## Repository Status

- **Main Branch**: Production-ready servers only
- **Feature Branches**: Development and experimental work
- **Automated Testing**: GitHub Actions for continuous integration
- **Platform**: Windows (Python 3.13.3), with Linux/Mac compatibility considerations
- **License**: Private/Proprietary
- **Maintained By**: Ruben Sanchez