# Google Drive MCP Server Fix - OAuth Authentication Required

## ISSUE IDENTIFIED
The @modelcontextprotocol/server-gdrive package requires OAuth 2.0 credentials, not service account credentials.

## COMPLETE FIX STEPS

### Step 1: Create OAuth 2.0 Credentials
1. Go to Google Cloud Console: https://console.cloud.google.com/
2. Navigate to: APIs & Services â†’ Credentials
3. Click "Create Credentials" â†’ "OAuth 2.0 Client IDs"
4. Application type: "Desktop application"  
5. Name: "Claude MCP Drive Access"
6. Click "Create"
7. Download the JSON file
8. Rename to: `gcp-oauth.keys.json`
9. Place in: `C:\Users\ruben\Claude Tools\config\gcp-oauth.keys.json`

### Step 2: Run Authentication Flow
Navigate to Claude Tools directory and run:
```bash
cd "C:\Users\ruben\Claude Tools"
set GDRIVE_OAUTH_PATH=C:\Users\ruben\Claude Tools\config\gcp-oauth.keys.json
set GDRIVE_CREDENTIALS_PATH=C:\Users\ruben\Claude Tools\config\.gdrive-server-credentials.json
npx -y @modelcontextprotocol/server-gdrive auth
```

### Step 3: Update Claude Desktop Config
After authentication succeeds, update config to point to the new credentials file:

```json
"gdrive": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-gdrive"],
  "env": {
    "GDRIVE_CREDENTIALS_PATH": "C:\\Users\\ruben\\Claude Tools\\config\\.gdrive-server-credentials.json"
  }
}
```

### Step 4: Restart Claude Desktop
Close and restart Claude Desktop to reload the MCP server with new authentication.

## WHY THIS FIX WORKS
- OAuth 2.0 allows interactive user authentication through browser
- Service accounts don't work with this particular MCP package
- The auth command generates proper credentials file for the MCP server
- Much simpler than service account + sharing workflow

## FILES INVOLVED
- OAuth keys: `C:\Users\ruben\Claude Tools\config\gcp-oauth.keys.json`
- Generated credentials: `C:\Users\ruben\Claude Tools\config\.gdrive-server-credentials.json`
- Claude config: `C:\Users\ruben\AppData\Roaming\Claude\claude_desktop_config.json`
