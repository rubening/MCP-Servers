# DEVELOPER TOOLS LIST (Developer Mode Configuration)
*MCP servers requiring Developer Mode setup via claude_desktop_config.json*

## DEVELOPER MODE CRITERIA CHECKLIST
**Use Developer Mode when the tool:**
- âœ“ Requires external APIs or internet access
- âœ“ Needs shared/centralized database
- âœ“ Complex multi-step workflows
- âœ“ Team/company shared service
- âœ“ Real-time data requirements
- âœ“ Centralized updates needed
- âœ“ Scalable server infrastructure

---

## CONFIRMED DEVELOPER MODE SERVERS

### **AI & INTELLIGENCE SERVICES**

#### **1. DEEPSEEK MCP**
- **Location**: `working-servers/ai-services/deepseek_mcp.py`
- **Purpose**: AI reasoning and chat via DeepSeek API
- **Why Developer Mode**: External API dependency, real-time AI
- **Team Value**: Shared AI reasoning capability
- **Requirements**: API keys, internet access

**Configuration Priority**: HIGH
**User Target**: Teams needing advanced AI reasoning

---

#### **2. PERSONAL KNOWLEDGE INTELLIGENCE**
- **Location**: `working-servers/ai-services/personal_knowledge_intelligence.py`
- **Purpose**: Intelligent knowledge capture and search
- **Why Developer Mode**: Database persistence, complex analysis
- **Team Value**: Shared organizational knowledge
- **Requirements**: Database storage, persistent memory

**Configuration Priority**: HIGH
**User Target**: Knowledge workers, research teams

---

### **PROJECT MANAGEMENT & OPTIMIZATION**

#### **3. MCP PROJECT OPTIMIZER**
- **Location**: `business-tools/mcp-project-optimizer/enhanced_server.py`
- **Purpose**: Advanced project analysis and optimization
- **Why Developer Mode**: Complex workflows, intelligence database
- **Team Value**: Centralized project intelligence
- **Requirements**: Persistent storage, analysis capabilities

**Configuration Priority**: HIGH
**User Target**: Project managers, development teams

---

#### **4. PROJECT MANAGEMENT MCP**
- **Location**: `servers/project-management-mcp/project_management_mcp.py`
- **Purpose**: Comprehensive project tracking with database
- **Why Developer Mode**: Shared project database, team coordination
- **Team Value**: Multi-user project management
- **Requirements**: SQLite database, persistent data

**Configuration Priority**: MEDIUM
**User Target**: Project teams, managers

---

### **DATA & SECURITY SERVICES**

#### **5. CHROMA SECURE SERVER**
- **Location**: `servers/chroma_secure_server.py`
- **Purpose**: Secure vector database for document storage
- **Why Developer Mode**: Database server, security requirements
- **Team Value**: Shared secure document intelligence
- **Requirements**: Vector database, authentication

**Configuration Priority**: HIGH
**User Target**: Legal teams, secure document management

---

#### **6. LEAD QUALIFICATION MCP**
- **Location**: `servers/lead-qualification-mcp/lead_qualification_mcp.py`
- **Purpose**: AI-powered lead qualification and CRM integration
- **Why Developer Mode**: Database, external integrations, workflows
- **Team Value**: Shared sales intelligence
- **Requirements**: Database, potential CRM APIs

**Configuration Priority**: MEDIUM
**User Target**: Sales teams, business development

---

### **GOOGLE SERVICES INTEGRATION**

#### **7. GOOGLE CALENDAR MCP**
- **Location**: `servers/google-calendar/google_calendar_server.py`
- **Purpose**: Google Calendar integration and management
- **Why Developer Mode**: External Google API, authentication
- **Team Value**: Shared calendar coordination
- **Requirements**: Google API credentials, OAuth

**Configuration Priority**: MEDIUM
**User Target**: Teams using Google Workspace

---

#### **8. GOOGLE SHEETS MCP**
- **Location**: `servers/google-sheets/google_sheets_server.py`  
- **Purpose**: Google Sheets data manipulation
- **Why Developer Mode**: External Google API, real-time data
- **Team Value**: Shared spreadsheet automation
- **Requirements**: Google API credentials, OAuth

**Configuration Priority**: MEDIUM
**User Target**: Data teams, Google Workspace users

---

#### **9. GOOGLE ADS MCP**
- **Location**: `servers/google-ads-mcp/server.py`
- **Purpose**: Google Ads campaign management
- **Why Developer Mode**: External API, advertising data
- **Team Value**: Shared marketing intelligence
- **Requirements**: Google Ads API, authentication

**Configuration Priority**: LOW
**User Target**: Marketing teams, advertising specialists

---

### **EXTERNAL SERVICES**

#### **10. WEB SEARCH MCP SERVER**
- **Location**: `external-services/web-search-mcp-server/index.js`
- **Purpose**: Web search capabilities via external APIs
- **Why Developer Mode**: Internet access, search APIs
- **Team Value**: Shared research capabilities
- **Requirements**: Search API keys, internet access

**Configuration Priority**: MEDIUM
**User Target**: Research teams, content creators

---

## DEVELOPER MODE CONFIGURATION STRATEGY

### Configuration File Management
**Location**: `configs/claude_desktop_config_TEST.json`
**Strategy**: Maintain separate configs for different environments

### Phase 1: Core Intelligence (Immediate Setup)
1. **Deepseek MCP** - AI reasoning foundation
2. **Personal Knowledge Intelligence** - Knowledge management
3. **Chroma Secure Server** - Document intelligence

### Phase 2: Project Management
4. **MCP Project Optimizer** - Advanced project intelligence
5. **Project Management MCP** - Team coordination

### Phase 3: External Integrations
6. **Google Calendar/Sheets** - Workspace integration
7. **Web Search MCP** - Research capabilities
8. **Lead Qualification** - Business intelligence

## CROSS-PLATFORM DEPLOYMENT

### Windows Configuration
**Primary Development Environment**
- **Config Location**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Python Environment**: Existing Python setup
- **Server Management**: Local development and testing

### Mac M4 Configuration  
**Production Deployment Target**
- **Config Location**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Python Environment**: M4-compatible Python installation
- **Server Management**: Production server deployment

## SERVER HOSTING STRATEGIES

### Local Development Servers
**For Development/Testing**
- Run servers locally during development
- Use localhost addresses in config
- Ideal for testing and validation

### Cloud/Remote Servers
**For Team Production Use**
- Deploy to cloud infrastructure (AWS, GCP, Azure)
- Use remote URLs in config
- Centralized team access
- Scalable and maintainable

### Hybrid Approach
**Recommended Strategy**
- **Local**: AI services, personal tools
- **Remote**: Team collaboration, shared databases
- **Flexible**: Easy switching between environments

## AUTHENTICATION & SECURITY

### API Key Management
- **Environment Variables**: Secure credential storage
- **Key Rotation**: Regular security updates
- **Team Access**: Shared vs individual credentials

### Database Security
- **Access Controls**: User authentication
- **Data Encryption**: At rest and in transit
- **Backup Strategy**: Regular data protection

### Network Security
- **HTTPS**: Encrypted connections
- **Firewall**: Controlled server access
- **Monitoring**: Security event logging

## MAINTENANCE & UPDATES

### Centralized Updates
**Major Advantage of Developer Mode**
- Update server once, all users benefit
- No individual client updates required
- Faster feature deployment

### Server Monitoring
- **Health Checks**: Server availability monitoring
- **Performance**: Response time tracking
- **Error Logging**: Issue identification and resolution

### Version Management
- **Server Versioning**: Track server releases
- **Config Versioning**: Manage configuration changes
- **Rollback Capability**: Quick recovery from issues

---

## DEPLOYMENT CHECKLIST

### Pre-Deployment
- [ ] Server testing in local environment
- [ ] API credential configuration
- [ ] Database initialization
- [ ] Security review
- [ ] Documentation completion

### Deployment
- [ ] Server hosting setup
- [ ] Configuration file updates
- [ ] Team access provisioning
- [ ] Initial testing with team
- [ ] Performance baseline establishment

### Post-Deployment
- [ ] User training and documentation
- [ ] Monitoring setup
- [ ] Feedback collection
- [ ] Iterative improvements
- [ ] Security auditing

---
*Last Updated: July 22, 2025*
*Developer Strategy: Centralized, scalable, team-focused*