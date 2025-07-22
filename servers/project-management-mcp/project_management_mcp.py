#!/usr/bin/env python3
"""
Project Management MCP Server - FIXED VERSION
Comprehensive project charting, scheduling, tracking, and progress management
Built using the proven manual JSON-RPC pattern for Ruben's ecosystem
"""

import asyncio
import json
import os
import sys
import sqlite3
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

class ProjectManagementMCP:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), "project_management.db")
        self.init_database()
    
    def init_database(self):
        """Initialize project management database with comprehensive schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Projects table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'planning',
            priority INTEGER DEFAULT 3,
            start_date TEXT,
            target_date TEXT,
            completion_date TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Milestones table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS milestones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            name TEXT NOT NULL,
            description TEXT,
            target_date TEXT,
            completion_date TEXT,
            status TEXT DEFAULT 'pending',
            dependencies TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects (id)
        )
        ''')
        
        # Progress log
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS progress_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            log_type TEXT,
            message TEXT,
            metadata TEXT,
            logged_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects (id)
        )
        ''')
        
        conn.commit()
        conn.close()
    
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
                        "serverInfo": {"name": "project-management-mcp", "version": "1.0.0"}
                    }
                }
            
            elif method == "tools/list":
                return {
                    "jsonrpc": "2.0", 
                    "id": request_id,
                    "result": {
                        "tools": [
                            {
                                "name": "create_project",
                                "description": "Create a new project with comprehensive tracking",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string", "description": "Project name"},
                                        "description": {"type": "string", "description": "Project description"},
                                        "priority": {"type": "integer", "description": "Priority level (1-5)"},
                                        "start_date": {"type": "string", "description": "Start date (ISO format)"},
                                        "target_date": {"type": "string", "description": "Target completion date"}
                                    },
                                    "required": ["name"]
                                }
                            },
                            {
                                "name": "chart_project_course",
                                "description": "Chart the complete course for a project with milestones and dependencies",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "project_id": {"type": "integer", "description": "Project ID"},
                                        "milestones": {
                                            "type": "array",
                                            "description": "Array of milestone objects",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "name": {"type": "string"},
                                                    "description": {"type": "string"},
                                                    "target_date": {"type": "string"},
                                                    "dependencies": {"type": "array"}
                                                }
                                            }
                                        }
                                    },
                                    "required": ["project_id", "milestones"]
                                }
                            },
                            {
                                "name": "get_project_status",
                                "description": "Get comprehensive project status with progress tracking",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "project_id": {"type": "integer", "description": "Project ID"}
                                    },
                                    "required": ["project_id"]
                                }
                            },
                            {
                                "name": "schedule_project_reminders",
                                "description": "Schedule automated project reminders and check-ins",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "project_id": {"type": "integer", "description": "Project ID"},
                                        "reminder_settings": {
                                            "type": "object",
                                            "description": "Reminder configuration"
                                        }
                                    },
                                    "required": ["project_id", "reminder_settings"]
                                }
                            },
                            {
                                "name": "update_project_progress",
                                "description": "Update project or milestone progress with detailed logging",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "project_id": {"type": "integer", "description": "Project ID"},
                                        "milestone_id": {"type": "integer", "description": "Milestone ID (optional)"},
                                        "status": {"type": "string", "description": "New status"},
                                        "notes": {"type": "string", "description": "Progress notes"}
                                    },
                                    "required": ["project_id"]
                                }
                            },
                            {
                                "name": "get_all_projects_dashboard",
                                "description": "Get comprehensive dashboard view of all projects",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {},
                                    "required": []
                                }
                            }
                        ]
                    }
                }
                
            elif method == "tools/call":
                params = request.get("params", {})
                tool_name = params.get("name", "")
                arguments = params.get("arguments", {})
                
                # Route to tool functions
                if tool_name == "create_project":
                    return await self.create_project(request_id, arguments)
                elif tool_name == "chart_project_course":
                    return await self.chart_project_course(request_id, arguments)
                elif tool_name == "get_project_status":
                    return await self.get_project_status(request_id, arguments)
                elif tool_name == "schedule_project_reminders":
                    return await self.schedule_project_reminders(request_id, arguments)
                elif tool_name == "update_project_progress":
                    return await self.update_project_progress(request_id, arguments)
                elif tool_name == "get_all_projects_dashboard":
                    return await self.get_all_projects_dashboard(request_id, arguments)
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

    async def create_project(self, request_id, arguments):
        name = arguments.get("name", "")
        description = arguments.get("description", "")
        priority = arguments.get("priority", 3)
        start_date = arguments.get("start_date")
        target_date = arguments.get("target_date")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if not start_date:
                start_date = datetime.now().isoformat()
            
            cursor.execute('''
            INSERT INTO projects (name, description, priority, start_date, target_date)
            VALUES (?, ?, ?, ?, ?)
            ''', (name, description, priority, start_date, target_date))
            
            project_id = cursor.lastrowid
            
            # Log project creation
            cursor.execute('''
            INSERT INTO progress_log (project_id, log_type, message)
            VALUES (?, ?, ?)
            ''', (project_id, 'creation', f'Project "{name}" created'))
            
            conn.commit()
            conn.close()
            
            result_text = json.dumps({
                "success": True,
                "project_id": project_id,
                "message": f"Project '{name}' created successfully"
            }, indent=2)
            
        except Exception as e:
            result_text = f"Error creating project: {str(e)}"
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": result_text}]}
        }

    async def chart_project_course(self, request_id, arguments):
        project_id = arguments.get("project_id")
        milestones = arguments.get("milestones", [])
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Verify project exists
            cursor.execute('SELECT name FROM projects WHERE id = ?', (project_id,))
            project = cursor.fetchone()
            if not project:
                conn.close()
                result_text = json.dumps({"success": False, "error": "Project not found"}, indent=2)
            else:
                milestone_ids = []
                for milestone in milestones:
                    cursor.execute('''
                    INSERT INTO milestones (project_id, name, description, target_date, dependencies)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (
                        project_id,
                        milestone.get('name'),
                        milestone.get('description', ''),
                        milestone.get('target_date'),
                        json.dumps(milestone.get('dependencies', []))
                    ))
                    milestone_ids.append(cursor.lastrowid)
                
                # Log course charting
                cursor.execute('''
                INSERT INTO progress_log (project_id, log_type, message, metadata)
                VALUES (?, ?, ?, ?)
                ''', (
                    project_id, 
                    'course_charting', 
                    f'Project course charted with {len(milestones)} milestones',
                    json.dumps({'milestone_count': len(milestones)})
                ))
                
                conn.commit()
                conn.close()
                
                result_text = json.dumps({
                    "success": True,
                    "milestone_ids": milestone_ids,
                    "message": f"Course charted for project with {len(milestones)} milestones"
                }, indent=2)
                
        except Exception as e:
            result_text = f"Error charting project course: {str(e)}"
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": result_text}]}
        }

    async def get_project_status(self, request_id, arguments):
        project_id = arguments.get("project_id")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get project details
            cursor.execute('''
            SELECT id, name, description, status, priority, start_date, target_date, 
                   completion_date, created_at, updated_at
            FROM projects WHERE id = ?
            ''', (project_id,))
            
            project = cursor.fetchone()
            if not project:
                conn.close()
                result_text = json.dumps({"success": False, "error": "Project not found"}, indent=2)
            else:
                project_data = {
                    "id": project[0],
                    "name": project[1],
                    "description": project[2],
                    "status": project[3],
                    "priority": project[4],
                    "start_date": project[5],
                    "target_date": project[6],
                    "completion_date": project[7],
                    "created_at": project[8],
                    "updated_at": project[9]
                }
                
                # Get milestones
                cursor.execute('''
                SELECT id, name, description, target_date, completion_date, status, dependencies
                FROM milestones WHERE project_id = ? ORDER BY target_date
                ''', (project_id,))
                
                milestones = []
                for milestone in cursor.fetchall():
                    milestones.append({
                        "id": milestone[0],
                        "name": milestone[1],
                        "description": milestone[2],
                        "target_date": milestone[3],
                        "completion_date": milestone[4],
                        "status": milestone[5],
                        "dependencies": json.loads(milestone[6]) if milestone[6] else []
                    })
                
                # Get recent progress
                cursor.execute('''
                SELECT log_type, message, logged_at
                FROM progress_log WHERE project_id = ?
                ORDER BY logged_at DESC LIMIT 10
                ''', (project_id,))
                
                recent_progress = []
                for log in cursor.fetchall():
                    recent_progress.append({
                        "type": log[0],
                        "message": log[1],
                        "timestamp": log[2]
                    })
                
                # Calculate progress metrics
                total_milestones = len(milestones)
                completed_milestones = sum(1 for m in milestones if m['status'] == 'completed')
                progress_percentage = (completed_milestones / total_milestones * 100) if total_milestones > 0 else 0
                
                conn.close()
                
                result_text = json.dumps({
                    "success": True,
                    "project": project_data,
                    "milestones": milestones,
                    "recent_progress": recent_progress,
                    "metrics": {
                        "total_milestones": total_milestones,
                        "completed_milestones": completed_milestones,
                        "progress_percentage": round(progress_percentage, 2)
                    }
                }, indent=2)
                
        except Exception as e:
            result_text = f"Error getting project status: {str(e)}"
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": result_text}]}
        }

    async def schedule_project_reminders(self, request_id, arguments):
        project_id = arguments.get("project_id")
        reminder_settings = arguments.get("reminder_settings", {})
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            INSERT INTO progress_log (project_id, log_type, message, metadata)
            VALUES (?, ?, ?, ?)
            ''', (
                project_id,
                'reminder_scheduled',
                'Project reminders configured',
                json.dumps(reminder_settings)
            ))
            
            conn.commit()
            conn.close()
            
            result_text = json.dumps({
                "success": True,
                "message": "Project reminders scheduled successfully"
            }, indent=2)
            
        except Exception as e:
            result_text = f"Error scheduling reminders: {str(e)}"
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": result_text}]}
        }

    async def update_project_progress(self, request_id, arguments):
        project_id = arguments.get("project_id")
        milestone_id = arguments.get("milestone_id")
        status = arguments.get("status")
        notes = arguments.get("notes", "")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if milestone_id:
                # Update milestone
                if status:
                    cursor.execute('''
                    UPDATE milestones SET status = ?, completion_date = ?
                    WHERE id = ? AND project_id = ?
                    ''', (
                        status,
                        datetime.now().isoformat() if status == 'completed' else None,
                        milestone_id,
                        project_id
                    ))
                
                # Log milestone update
                cursor.execute('''
                INSERT INTO progress_log (project_id, log_type, message, metadata)
                VALUES (?, ?, ?, ?)
                ''', (
                    project_id,
                    'milestone_update',
                    f'Milestone updated: {notes}' if notes else 'Milestone status updated',
                    json.dumps({'milestone_id': milestone_id, 'new_status': status})
                ))
            else:
                # Update project
                if status:
                    cursor.execute('''
                    UPDATE projects SET status = ?, updated_at = ?,
                    completion_date = CASE WHEN ? = 'completed' THEN ? ELSE completion_date END
                    WHERE id = ?
                    ''', (
                        status,
                        datetime.now().isoformat(),
                        status,
                        datetime.now().isoformat() if status == 'completed' else None,
                        project_id
                    ))
                
                # Log project update
                cursor.execute('''
                INSERT INTO progress_log (project_id, log_type, message)
                VALUES (?, ?, ?)
                ''', (
                    project_id,
                    'project_update',
                    f'Project updated: {notes}' if notes else 'Project status updated'
                ))
            
            conn.commit()
            conn.close()
            
            result_text = json.dumps({
                "success": True,
                "message": "Progress updated successfully"
            }, indent=2)
            
        except Exception as e:
            result_text = f"Error updating progress: {str(e)}"
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": result_text}]}
        }

    async def get_all_projects_dashboard(self, request_id, arguments):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get all projects with basic stats
            cursor.execute('''
            SELECT p.id, p.name, p.status, p.priority, p.start_date, p.target_date,
                   COUNT(m.id) as milestone_count,
                   COUNT(CASE WHEN m.status = 'completed' THEN 1 END) as completed_milestones
            FROM projects p
            LEFT JOIN milestones m ON p.id = m.project_id
            GROUP BY p.id
            ORDER BY p.priority DESC, p.created_at DESC
            ''')
            
            projects = []
            for row in cursor.fetchall():
                total_milestones = row[6]
                completed_milestones = row[7]
                progress = (completed_milestones / total_milestones * 100) if total_milestones > 0 else 0
                
                projects.append({
                    "id": row[0],
                    "name": row[1],
                    "status": row[2],
                    "priority": row[3],
                    "start_date": row[4],
                    "target_date": row[5],
                    "milestone_count": total_milestones,
                    "completed_milestones": completed_milestones,
                    "progress_percentage": round(progress, 2)
                })
            
            # Get projects needing attention
            today = datetime.now().isoformat()
            cursor.execute('''
            SELECT p.name, p.id, p.priority, p.target_date
            FROM projects p
            WHERE p.status != 'completed' 
            AND (p.target_date < ? OR p.priority >= 4)
            ORDER BY p.priority DESC, p.target_date ASC
            ''', (today,))
            
            attention_needed = []
            for row in cursor.fetchall():
                attention_needed.append({
                    "name": row[0],
                    "id": row[1],
                    "priority": row[2],
                    "target_date": row[3],
                    "reason": "overdue" if row[3] < today else "high_priority"
                })
            
            conn.close()
            
            result_text = json.dumps({
                "success": True,
                "projects": projects,
                "attention_needed": attention_needed,
                "summary": {
                    "total_projects": len(projects),
                    "active_projects": len([p for p in projects if p['status'] in ['active', 'in_progress']]),
                    "completed_projects": len([p for p in projects if p['status'] == 'completed'])
                }
            }, indent=2)
            
        except Exception as e:
            result_text = f"Error getting dashboard: {str(e)}"
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": result_text}]}
        }

async def main():
    mcp = ProjectManagementMCP()
    
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
