#!/usr/bin/env python3
"""
Google Calendar MCP Server
Provides calendar management capabilities with attorney-client privilege protection.
"""

import asyncio
import json
import logging
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Sequence

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, TextContent, ImageContent, EmbeddedResource

# Google Calendar API imports
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
logger = logging.getLogger("google-calendar-mcp")

class GoogleCalendarMCP:
    def __init__(self, credentials_path: str):
        """Initialize Google Calendar MCP with service account credentials."""
        self.credentials_path = credentials_path
        self.service = None
        self._initialize_service()
    
    def _initialize_service(self):
        """Initialize Google Calendar service with authentication."""
        try:
            # Load service account credentials
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=['https://www.googleapis.com/auth/calendar']
            )
            
            # Build the Calendar service
            self.service = build('calendar', 'v3', credentials=credentials)
            logger.info("Google Calendar service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Google Calendar service: {e}")
            raise
    
    async def list_calendars(self) -> List[Dict[str, Any]]:
        """List all calendars accessible to the service account."""
        try:
            result = self.service.calendarList().list().execute()
            calendars = result.get('items', [])
            
            return [{
                'id': cal.get('id'),
                'summary': cal.get('summary'),
                'description': cal.get('description', ''),
                'primary': cal.get('primary', False),
                'accessRole': cal.get('accessRole'),
                'timeZone': cal.get('timeZone')
            } for cal in calendars]
            
        except HttpError as e:
            logger.error(f"Failed to list calendars: {e}")
            return []
    
    async def list_events(self, calendar_id: str = 'primary', 
                         time_min: Optional[str] = None,
                         time_max: Optional[str] = None,
                         max_results: int = 50) -> List[Dict[str, Any]]:
        """List events from a specific calendar."""
        try:
            # Set default time range if not provided
            if not time_min:
                time_min = datetime.utcnow().isoformat() + 'Z'
            if not time_max:
                future_date = datetime.utcnow() + timedelta(days=30)
                time_max = future_date.isoformat() + 'Z'
            
            result = self.service.events().list(
                calendarId=calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = result.get('items', [])
            
            return [{
                'id': event.get('id'),
                'summary': event.get('summary'),
                'description': event.get('description', ''),
                'start': event.get('start'),
                'end': event.get('end'),
                'location': event.get('location', ''),
                'attendees': event.get('attendees', []),
                'status': event.get('status'),
                'htmlLink': event.get('htmlLink')
            } for event in events]
            
        except HttpError as e:
            logger.error(f"Failed to list events: {e}")
            return []
    
    async def create_event(self, calendar_id: str = 'primary', 
                          summary: str = '', description: str = '',
                          start_time: str = '', end_time: str = '',
                          location: str = '', attendees: List[str] = None) -> Dict[str, Any]:
        """Create a new calendar event."""
        try:
            event_body = {
                'summary': summary,
                'description': description,
                'start': {
                    'dateTime': start_time,
                    'timeZone': 'America/Chicago',  # Ruben's timezone
                },
                'end': {
                    'dateTime': end_time,
                    'timeZone': 'America/Chicago',
                },
            }
            
            if location:
                event_body['location'] = location
            
            if attendees:
                event_body['attendees'] = [{'email': email} for email in attendees]
            
            event = self.service.events().insert(
                calendarId=calendar_id,
                body=event_body
            ).execute()
            
            return {
                'id': event.get('id'),
                'summary': event.get('summary'),
                'htmlLink': event.get('htmlLink'),
                'status': 'created'
            }
            
        except HttpError as e:
            logger.error(f"Failed to create event: {e}")
            return {'error': str(e)}
    
    async def update_event(self, calendar_id: str, event_id: str,
                          summary: str = None, description: str = None,
                          start_time: str = None, end_time: str = None) -> Dict[str, Any]:
        """Update an existing calendar event."""
        try:
            # Get current event
            event = self.service.events().get(
                calendarId=calendar_id,
                eventId=event_id
            ).execute()
            
            # Update fields
            if summary:
                event['summary'] = summary
            if description:
                event['description'] = description
            if start_time:
                event['start']['dateTime'] = start_time
            if end_time:
                event['end']['dateTime'] = end_time
            
            updated_event = self.service.events().update(
                calendarId=calendar_id,
                eventId=event_id,
                body=event
            ).execute()
            
            return {
                'id': updated_event.get('id'),
                'summary': updated_event.get('summary'),
                'status': 'updated'
            }
            
        except HttpError as e:
            logger.error(f"Failed to update event: {e}")
            return {'error': str(e)}
    
    async def delete_event(self, calendar_id: str, event_id: str) -> Dict[str, Any]:
        """Delete a calendar event."""
        try:
            self.service.events().delete(
                calendarId=calendar_id,
                eventId=event_id
            ).execute()
            
            return {'status': 'deleted', 'eventId': event_id}
            
        except HttpError as e:
            logger.error(f"Failed to delete event: {e}")
            return {'error': str(e)}

# Initialize the MCP server
app = Server("google-calendar")
calendar_mcp = None

@app.list_tools()
async def list_tools() -> List[Tool]:
    """List available Google Calendar tools."""
    return [
        Tool(
            name="list_calendars",
            description="List all accessible Google Calendars",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="list_events",
            description="List events from a calendar with optional time filtering",
            inputSchema={
                "type": "object", 
                "properties": {
                    "calendar_id": {
                        "type": "string",
                        "description": "Calendar ID (default: 'primary')",
                        "default": "primary"
                    },
                    "time_min": {
                        "type": "string",
                        "description": "Start time filter (ISO format)"
                    },
                    "time_max": {
                        "type": "string", 
                        "description": "End time filter (ISO format)"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of events (default: 50)",
                        "default": 50
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="create_event",
            description="Create a new calendar event",
            inputSchema={
                "type": "object",
                "properties": {
                    "calendar_id": {
                        "type": "string", 
                        "description": "Calendar ID (default: 'primary')",
                        "default": "primary"
                    },
                    "summary": {
                        "type": "string",
                        "description": "Event title/summary"
                    },
                    "description": {
                        "type": "string",
                        "description": "Event description"
                    },
                    "start_time": {
                        "type": "string",
                        "description": "Start time (ISO format)"
                    },
                    "end_time": {
                        "type": "string",
                        "description": "End time (ISO format)"
                    },
                    "location": {
                        "type": "string",
                        "description": "Event location"
                    },
                    "attendees": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of attendee email addresses"
                    }
                },
                "required": ["summary", "start_time", "end_time"]
            }
        ),
        Tool(
            name="update_event", 
            description="Update an existing calendar event",
            inputSchema={
                "type": "object",
                "properties": {
                    "calendar_id": {
                        "type": "string",
                        "description": "Calendar ID"
                    },
                    "event_id": {
                        "type": "string", 
                        "description": "Event ID to update"
                    },
                    "summary": {
                        "type": "string",
                        "description": "New event title/summary"
                    },
                    "description": {
                        "type": "string",
                        "description": "New event description"
                    },
                    "start_time": {
                        "type": "string",
                        "description": "New start time (ISO format)"
                    },
                    "end_time": {
                        "type": "string",
                        "description": "New end time (ISO format)"
                    }
                },
                "required": ["calendar_id", "event_id"]
            }
        ),
        Tool(
            name="delete_event",
            description="Delete a calendar event",
            inputSchema={
                "type": "object",
                "properties": {
                    "calendar_id": {
                        "type": "string",
                        "description": "Calendar ID"
                    },
                    "event_id": {
                        "type": "string",
                        "description": "Event ID to delete" 
                    }
                },
                "required": ["calendar_id", "event_id"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle tool calls for Google Calendar operations."""
    try:
        if name == "list_calendars":
            calendars = await calendar_mcp.list_calendars()
            return [TextContent(
                type="text",
                text=json.dumps(calendars, indent=2)
            )]
        
        elif name == "list_events":
            events = await calendar_mcp.list_events(
                calendar_id=arguments.get("calendar_id", "primary"),
                time_min=arguments.get("time_min"),
                time_max=arguments.get("time_max"), 
                max_results=arguments.get("max_results", 50)
            )
            return [TextContent(
                type="text",
                text=json.dumps(events, indent=2)
            )]
        
        elif name == "create_event":
            result = await calendar_mcp.create_event(
                calendar_id=arguments.get("calendar_id", "primary"),
                summary=arguments.get("summary", ""),
                description=arguments.get("description", ""),
                start_time=arguments.get("start_time", ""),
                end_time=arguments.get("end_time", ""),
                location=arguments.get("location", ""),
                attendees=arguments.get("attendees", [])
            )
            return [TextContent(
                type="text", 
                text=json.dumps(result, indent=2)
            )]
        
        elif name == "update_event":
            result = await calendar_mcp.update_event(
                calendar_id=arguments.get("calendar_id"),
                event_id=arguments.get("event_id"),
                summary=arguments.get("summary"),
                description=arguments.get("description"),
                start_time=arguments.get("start_time"),
                end_time=arguments.get("end_time")
            )
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        elif name == "delete_event":
            result = await calendar_mcp.delete_event(
                calendar_id=arguments.get("calendar_id"),
                event_id=arguments.get("event_id")
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
    """Main entry point for the Google Calendar MCP server."""
    global calendar_mcp
    
    # Get credentials path from command line or default
    credentials_path = "C:\\Users\\ruben\\Claude Tools\\config\\gdrive-credentials.json"
    if len(sys.argv) > 1:
        credentials_path = sys.argv[1]
    
    # Initialize Google Calendar MCP
    try:
        calendar_mcp = GoogleCalendarMCP(credentials_path)
        logger.info("Google Calendar MCP server starting...")
        
        # Run the server
        async with stdio_server() as streams:
            await app.run(streams[0], streams[1], app.create_initialization_options())
            
    except Exception as e:
        logger.error(f"Failed to start Google Calendar MCP server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
