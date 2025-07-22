# MCP SERVER MASTER MANIFEST
*Comprehensive index of all MCP servers for categorization analysis*

## PURPOSE
This manifest provides a complete inventory of all MCP servers in this repository for the Extension vs Developer Mode categorization strategy. Each server is analyzed for optimal deployment method.

## CATEGORIZATION CRITERIA SUMMARY
**Extension (.dxt)**: Simple, local tools, easy distribution, self-contained
**Developer Mode**: Complex tools, external APIs, databases, team sharing

---

## ACTIVE WORKING SERVERS (Production Ready)

### Core Infrastructure
| Server | Location | Status | Category TBD |
|--------|----------|--------|--------------|
| **filesystem_mcp** | `working-servers-backup/core-infrastructure/` | Production | Extension Candidate |
| **git_mcp** | `working-servers-backup/core-infrastructure/` | Production | Extension Candidate |
| **execute_command_mcp** | `working-servers/core-infrastructure/` | Production | Extension Candidate |

### AI & Intelligence Services  
| Server | Location | Status | Category TBD |
|--------|----------|--------|--------------|
| **deepseek_mcp** | `working-servers/ai-services/` | Production | Developer Mode |
| **personal_knowledge_intelligence** | `working-servers/ai-services/` | Production | Developer Mode |

### Analytics & Media
| Server | Location | Status | Category TBD |
|--------|----------|--------|--------------|
| **duckdb_analytics** | `working-servers/analytics-media/` | Production | Extension Candidate |

### Business Tools
| Server | Location | Status | Category TBD |
|--------|----------|--------|--------------|
| **project_instructions_generator** | `servers/` | Production | Extension Candidate |
| **youtube_mcp** | `servers/` | Production | Extension Candidate |

---

## DEVELOPMENT & SPECIALIZED SERVERS

### Project Management
| Server | Location | Status | Category TBD |
|--------|----------|--------|--------------|
| **project-management-mcp** | `servers/project-management-mcp/` | Development | Developer Mode |
| **mcp-project-optimizer** | `business-tools/mcp-project-optimizer/` | Enhanced | Developer Mode |
| **priority-management** | `business-tools/priority-management/` | Development | Extension Candidate |

### Data & Security
| Server | Location | Status | Category TBD |
|--------|----------|--------|--------------|
| **chroma_secure_server** | `servers/` | Development | Developer Mode |
| **lead-qualification-mcp** | `servers/lead-qualification-mcp/` | Specialized | Developer Mode |

### Google Services Integration
| Server | Location | Status | Category TBD |
|--------|----------|--------|--------------|
| **google-calendar** | `servers/google-calendar/` | Development | Developer Mode |
| **google-sheets** | `servers/google-sheets/` | Development | Developer Mode |
| **google-ads-mcp** | `servers/google-ads-mcp/` | Development | Developer Mode |

### External Services
| Server | Location | Status | Category TBD |
|--------|----------|--------|--------------|
| **web-search-mcp-server** | `external-services/web-search-mcp-server/` | Development | Developer Mode |

---

## CATEGORIZATION STATUS
- **Analysis Pending**: 16 servers identified
- **Extension Candidates**: 6 servers (local, simple tools)
- **Developer Mode**: 10 servers (complex, external dependencies)

## CROSS-PLATFORM CONSIDERATIONS
- **Windows Primary**: Development and testing environment
- **Mac M4 Target**: Production deployment environment
- **Sync Strategy**: Required for both platforms

## NEXT ACTIONS
1. Create categorization manifests
2. Analyze each server against criteria
3. Test cross-platform compatibility
4. Document deployment strategies

---
*Last Updated: July 22, 2025*
*Repository: C:\Users\ruben\OneDrive\MCP_Servers*