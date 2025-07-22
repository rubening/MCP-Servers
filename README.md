# MCP Server Repository
*Model Context Protocol Server Management Platform*

## Overview

This repository manages our complete MCP (Model Context Protocol) server ecosystem, providing organized storage, version control, and deployment management for all server components.

## Repository Structure

### Core Infrastructure
**Location:** `core-infrastructure/`
Essential servers providing basic functionality:
- **filesystem** - File and directory operations
- **execute-command** - Shell command execution
- **git** - Version control operations  
- **youtube** - Video processing and management

### External Services
**Location:** `external-services/`
Third-party service integrations:
- **mcp-github** - GitHub API integration
- **clickup** - Project management integration
- **gdrive** - Google Drive operations
- **n8n-mcp** - Workflow automation
- **playwright** - Web automation and testing

### Analytics & Intelligence
**Location:** `analytics-intelligence/`
Data analysis and knowledge management:
- **e5-marketing-research** - Marketing intelligence
- **personal-knowledge-intelligence** - Knowledge capture and retrieval
- **duckdb-analytics** - Business intelligence and analytics
- **chroma-secure** - Vector database for secure data

### AI & Reasoning
**Location:** `ai-reasoning/`
AI-powered analysis and reasoning tools:
- **deepseek** - Advanced reasoning and chat capabilities

### Business Tools
**Location:** `business-tools/`
Business process and workflow management:
- **lead-qualification** - Lead scoring and qualification
- **project-management** - Project tracking and management
- **project-instructions-generator** - Project documentation automation

### Tony Ramos Law
**Location:** `tony-ramos-law/`
Client-specific tools and integrations:
- **swiss-army-knife-copywriter** - Perry Marshall copywriting methodology
- **google-ads-mcp** - Specialized Google Ads campaign generation

### Experimental
**Location:** `experimental/`
Servers under development and testing:
- **mcp-project-optimizer** - Project analysis and optimization
- **web-search-mcp-server** - Web search capabilities
- **priority-management** - Priority and task management

### Archived
**Location:** `archived/`
Deprecated servers maintained for reference

## Quick Start

### Prerequisites
- Python 3.8+ with MCP support
- Node.js 16+ (for Node.js-based servers)
- Git for version control
- Required API keys (see individual server documentation)

### Installation
1. Clone this repository
2. Navigate to desired server directory
3. Install dependencies: `pip install -r requirements.txt` or `npm install`
4. Configure environment variables
5. Add server to Claude Desktop configuration

### Configuration
Update your Claude Desktop configuration (`claude_desktop_config.json`) with server paths and environment variables. See individual server directories for specific configuration requirements.

## Development Workflow

### Experimental Server Promotion
1. **Development**: Create in `experimental/` directory
2. **Testing**: Run comprehensive test suites
3. **Documentation**: Complete README and API documentation
4. **Review**: Code review and performance validation
5. **Promotion**: Move to appropriate category directory
6. **Integration**: Update main configuration and deploy

### Version Control
- **Main branch**: Production-ready servers only
- **Feature branches**: Development and experimental work
- **Tags**: Release versions and stable snapshots
- **Automated testing**: GitHub Actions for continuous integration

## Backup and Recovery

### Automated Backups
- **Nightly**: Full repository backup to OneDrive
- **Weekly**: Complete system snapshots
- **Monthly**: Archive and cleanup old versions

### Recovery Procedures
1. Restore from GitHub main branch for code
2. Restore databases from latest backup snapshots
3. Reconfigure environment variables and API keys
4. Verify server connectivity and functionality

## Security

### API Key Management
- Never commit API keys to version control
- Use environment variables for sensitive data
- Rotate keys regularly
- Monitor access and usage

### Access Control
- Private repository with restricted access
- Two-factor authentication required
- Signed commits for production changes
- Regular security audits

## Contributing

### Code Standards
- Follow Python PEP 8 and JavaScript Standard Style
- Include comprehensive test coverage
- Document all public APIs
- Use semantic versioning for releases

### Testing Requirements
- Unit tests for all functions
- Integration tests for external services
- Performance benchmarks for optimization
- Security testing for sensitive operations

## Support

### Documentation
- Individual server README files
- API documentation in `/docs`
- Troubleshooting guides
- Configuration examples

### Issue Tracking
- GitHub Issues for bug reports
- Feature requests via GitHub Discussions
- Security issues via private disclosure

---

**Repository Status**: Active Development  
**Last Updated**: July 22, 2025  
**Maintained By**: Ruben Sanchez  
**License**: Private/Proprietary
