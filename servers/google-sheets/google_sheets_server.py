#!/usr/bin/env python3
"""
Google Sheets MCP Server
Provides spreadsheet management capabilities with attorney-client privilege protection.
"""

import asyncio
import json
import logging
import sys
from typing import Any, Dict, List, Optional, Sequence

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, TextContent, ImageContent, EmbeddedResource

# Google Sheets API imports
try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError as e:
    print(f"Error: Missing required Google API libraries: {e}")
    print("Install with: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("google-sheets-mcp")

class GoogleSheetsMCP:
    def __init__(self, credentials_path: str):
        """Initialize Google Sheets MCP with service account credentials."""
        self.credentials_path = credentials_path
        self.service = None
        self.drive_service = None
        self._initialize_service()
    
    def _initialize_service(self):
        """Initialize Google Sheets service with authentication."""
        try:
            # Load service account credentials
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=[
                    'https://www.googleapis.com/auth/spreadsheets',
                    'https://www.googleapis.com/auth/drive'
                ]
            )
            
            # Build the Sheets and Drive services
            self.service = build('sheets', 'v4', credentials=credentials)
            self.drive_service = build('drive', 'v3', credentials=credentials)
            logger.info("Google Sheets service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Google Sheets service: {e}")
            raise
    
    async def list_spreadsheets(self, query: str = "mimeType='application/vnd.google-apps.spreadsheet'") -> List[Dict[str, Any]]:
        """List all spreadsheets accessible to the service account."""
        try:
            result = self.drive_service.files().list(
                q=query,
                fields="files(id, name, createdTime, modifiedTime, owners, shared, webViewLink)"
            ).execute()
            
            files = result.get('files', [])
            
            return [{
                'id': file.get('id'),
                'name': file.get('name'),
                'createdTime': file.get('createdTime'),
                'modifiedTime': file.get('modifiedTime'),
                'owners': file.get('owners', []),
                'shared': file.get('shared', False),
                'webViewLink': file.get('webViewLink')
            } for file in files]
            
        except HttpError as e:
            logger.error(f"Failed to list spreadsheets: {e}")
            return []
    
    async def get_spreadsheet_info(self, spreadsheet_id: str) -> Dict[str, Any]:
        """Get detailed information about a spreadsheet."""
        try:
            result = self.service.spreadsheets().get(
                spreadsheetId=spreadsheet_id
            ).execute()
            
            return {
                'id': result.get('spreadsheetId'),
                'title': result.get('properties', {}).get('title'),
                'sheets': [{
                    'id': sheet.get('properties', {}).get('sheetId'),
                    'title': sheet.get('properties', {}).get('title'),
                    'gridProperties': sheet.get('properties', {}).get('gridProperties', {})
                } for sheet in result.get('sheets', [])]
            }
            
        except HttpError as e:
            logger.error(f"Failed to get spreadsheet info: {e}")
            return {}
    
    async def read_range(self, spreadsheet_id: str, range_name: str) -> Dict[str, Any]:
        """Read data from a specific range in a spreadsheet."""
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()
            
            return {
                'range': result.get('range'),
                'majorDimension': result.get('majorDimension'),
                'values': result.get('values', [])
            }
            
        except HttpError as e:
            logger.error(f"Failed to read range: {e}")
            return {}
    
    async def write_range(self, spreadsheet_id: str, range_name: str, 
                         values: List[List[Any]], value_input_option: str = 'RAW') -> Dict[str, Any]:
        """Write data to a specific range in a spreadsheet."""
        try:
            body = {
                'values': values
            }
            
            result = self.service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body
            ).execute()
            
            return {
                'updatedCells': result.get('updatedCells'),
                'updatedColumns': result.get('updatedColumns'),
                'updatedRows': result.get('updatedRows'),
                'updatedRange': result.get('updatedRange')
            }
            
        except HttpError as e:
            logger.error(f"Failed to write range: {e}")
            return {'error': str(e)}
    
    async def append_data(self, spreadsheet_id: str, range_name: str,
                         values: List[List[Any]], value_input_option: str = 'RAW') -> Dict[str, Any]:
        """Append data to a spreadsheet."""
        try:
            body = {
                'values': values
            }
            
            result = self.service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body
            ).execute()
            
            return {
                'spreadsheetId': result.get('spreadsheetId'),
                'updatedRange': result.get('updates', {}).get('updatedRange'),
                'updatedRows': result.get('updates', {}).get('updatedRows'),
                'updatedColumns': result.get('updates', {}).get('updatedColumns')
            }
            
        except HttpError as e:
            logger.error(f"Failed to append data: {e}")
            return {'error': str(e)}
    
    async def create_spreadsheet(self, title: str, sheets: List[str] = None) -> Dict[str, Any]:
        """Create a new spreadsheet."""
        try:
            body = {
                'properties': {
                    'title': title
                }
            }
            
            # Add custom sheets if specified
            if sheets:
                body['sheets'] = []
                for sheet_title in sheets:
                    body['sheets'].append({
                        'properties': {
                            'title': sheet_title
                        }
                    })
            
            result = self.service.spreadsheets().create(body=body).execute()
            
            return {
                'id': result.get('spreadsheetId'),
                'title': result.get('properties', {}).get('title'),
                'url': result.get('spreadsheetUrl')
            }
            
        except HttpError as e:
            logger.error(f"Failed to create spreadsheet: {e}")
            return {'error': str(e)}
    
    async def add_sheet(self, spreadsheet_id: str, sheet_title: str) -> Dict[str, Any]:
        """Add a new sheet to an existing spreadsheet."""
        try:
            body = {
                'requests': [{
                    'addSheet': {
                        'properties': {
                            'title': sheet_title
                        }
                    }
                }]
            }
            
            result = self.service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body=body
            ).execute()
            
            return {
                'sheetId': result.get('replies', [{}])[0].get('addSheet', {}).get('properties', {}).get('sheetId'),
                'title': sheet_title,
                'status': 'created'
            }
            
        except HttpError as e:
            logger.error(f"Failed to add sheet: {e}")
            return {'error': str(e)}
    
    async def clear_range(self, spreadsheet_id: str, range_name: str) -> Dict[str, Any]:
        """Clear data from a specific range."""
        try:
            result = self.service.spreadsheets().values().clear(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()
            
            return {
                'clearedRange': result.get('clearedRange'),
                'status': 'cleared'
            }
            
        except HttpError as e:
            logger.error(f"Failed to clear range: {e}")
            return {'error': str(e)}

# Initialize the MCP server
app = Server("google-sheets")
sheets_mcp = None

@app.list_tools()
async def list_tools() -> List[Tool]:
    """List available Google Sheets tools."""
    return [
        Tool(
            name="list_spreadsheets",
            description="List all accessible Google Spreadsheets",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Drive API query filter (default: all spreadsheets)",
                        "default": "mimeType='application/vnd.google-apps.spreadsheet'"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_spreadsheet_info",
            description="Get detailed information about a specific spreadsheet",
            inputSchema={
                "type": "object",
                "properties": {
                    "spreadsheet_id": {
                        "type": "string",
                        "description": "The ID of the spreadsheet"
                    }
                },
                "required": ["spreadsheet_id"]
            }
        ),
        Tool(
            name="read_range",
            description="Read data from a specific range in a spreadsheet",
            inputSchema={
                "type": "object",
                "properties": {
                    "spreadsheet_id": {
                        "type": "string",
                        "description": "The ID of the spreadsheet"
                    },
                    "range_name": {
                        "type": "string",
                        "description": "The range to read (e.g., 'Sheet1!A1:C10')"
                    }
                },
                "required": ["spreadsheet_id", "range_name"]
            }
        ),
        Tool(
            name="write_range",
            description="Write data to a specific range in a spreadsheet",
            inputSchema={
                "type": "object",
                "properties": {
                    "spreadsheet_id": {
                        "type": "string",
                        "description": "The ID of the spreadsheet"
                    },
                    "range_name": {
                        "type": "string",
                        "description": "The range to write to (e.g., 'Sheet1!A1:C10')"
                    },
                    "values": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "description": "2D array of values to write"
                    },
                    "value_input_option": {
                        "type": "string",
                        "enum": ["RAW", "USER_ENTERED"],
                        "description": "How to interpret input values",
                        "default": "RAW"
                    }
                },
                "required": ["spreadsheet_id", "range_name", "values"]
            }
        ),
        Tool(
            name="append_data",
            description="Append data to a spreadsheet",
            inputSchema={
                "type": "object",
                "properties": {
                    "spreadsheet_id": {
                        "type": "string",
                        "description": "The ID of the spreadsheet"
                    },
                    "range_name": {
                        "type": "string",
                        "description": "The range to append to (e.g., 'Sheet1!A:C')"
                    },
                    "values": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "description": "2D array of values to append"
                    },
                    "value_input_option": {
                        "type": "string",
                        "enum": ["RAW", "USER_ENTERED"],
                        "description": "How to interpret input values",
                        "default": "RAW"
                    }
                },
                "required": ["spreadsheet_id", "range_name", "values"]
            }
        ),
        Tool(
            name="create_spreadsheet",
            description="Create a new spreadsheet",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Title of the new spreadsheet"
                    },
                    "sheets": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of sheet names to create (optional)"
                    }
                },
                "required": ["title"]
            }
        ),
        Tool(
            name="add_sheet",
            description="Add a new sheet to an existing spreadsheet",
            inputSchema={
                "type": "object",
                "properties": {
                    "spreadsheet_id": {
                        "type": "string",
                        "description": "The ID of the spreadsheet"
                    },
                    "sheet_title": {
                        "type": "string",
                        "description": "Title of the new sheet"
                    }
                },
                "required": ["spreadsheet_id", "sheet_title"]
            }
        ),
        Tool(
            name="clear_range",
            description="Clear data from a specific range",
            inputSchema={
                "type": "object",
                "properties": {
                    "spreadsheet_id": {
                        "type": "string",
                        "description": "The ID of the spreadsheet"
                    },
                    "range_name": {
                        "type": "string",
                        "description": "The range to clear (e.g., 'Sheet1!A1:C10')"
                    }
                },
                "required": ["spreadsheet_id", "range_name"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle tool calls for Google Sheets operations."""
    try:
        if name == "list_spreadsheets":
            spreadsheets = await sheets_mcp.list_spreadsheets(
                query=arguments.get("query", "mimeType='application/vnd.google-apps.spreadsheet'")
            )
            return [TextContent(
                type="text",
                text=json.dumps(spreadsheets, indent=2)
            )]
        
        elif name == "get_spreadsheet_info":
            info = await sheets_mcp.get_spreadsheet_info(
                spreadsheet_id=arguments.get("spreadsheet_id")
            )
            return [TextContent(
                type="text",
                text=json.dumps(info, indent=2)
            )]
        
        elif name == "read_range":
            data = await sheets_mcp.read_range(
                spreadsheet_id=arguments.get("spreadsheet_id"),
                range_name=arguments.get("range_name")
            )
            return [TextContent(
                type="text",
                text=json.dumps(data, indent=2)
            )]
        
        elif name == "write_range":
            result = await sheets_mcp.write_range(
                spreadsheet_id=arguments.get("spreadsheet_id"),
                range_name=arguments.get("range_name"),
                values=arguments.get("values"),
                value_input_option=arguments.get("value_input_option", "RAW")
            )
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        elif name == "append_data":
            result = await sheets_mcp.append_data(
                spreadsheet_id=arguments.get("spreadsheet_id"),
                range_name=arguments.get("range_name"),
                values=arguments.get("values"),
                value_input_option=arguments.get("value_input_option", "RAW")
            )
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        elif name == "create_spreadsheet":
            result = await sheets_mcp.create_spreadsheet(
                title=arguments.get("title"),
                sheets=arguments.get("sheets")
            )
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        elif name == "add_sheet":
            result = await sheets_mcp.add_sheet(
                spreadsheet_id=arguments.get("spreadsheet_id"),
                sheet_title=arguments.get("sheet_title")
            )
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        elif name == "clear_range":
            result = await sheets_mcp.clear_range(
                spreadsheet_id=arguments.get("spreadsheet_id"),
                range_name=arguments.get("range_name")
            )
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]
            
    except Exception as e:
        logger.error(f"Error in {name}: {e}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]

async def main():
    """Main entry point for the Google Sheets MCP server."""
    global sheets_mcp
    
    # Get credentials path from command line or default
    credentials_path = "C:\\Users\\ruben\\Claude Tools\\config\\gdrive-credentials.json"
    if len(sys.argv) > 1:
        credentials_path = sys.argv[1]
    
    # Initialize Google Sheets MCP
    try:
        sheets_mcp = GoogleSheetsMCP(credentials_path)
        logger.info("Google Sheets MCP server starting...")
        
        # Run the server
        async with stdio_server() as streams:
            await app.run(streams[0], streams[1], app.create_initialization_options())
            
    except Exception as e:
        logger.error(f"Failed to start Google Sheets MCP server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
