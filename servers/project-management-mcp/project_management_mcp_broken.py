#!/usr/bin/env python3
"""
Project Management MCP Server - FIXED VERSION
Comprehensive project charting, scheduling, tracking, and progress management
Built using the proven manual JSON-RPC pattern for Ruben's ecosystem
"""

import json
import sys
import asyncio
import os
from datetime import datetime, timedelta
import sqlite3
from typing import Dict, List, Any, Optional

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
        
        # Tasks table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            milestone_id INTEGER,
            name TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'todo',
            priority INTEGER DEFAULT 3,
            estimated_hours REAL,
            actual_hours REAL,
            assigned_to TEXT,
            due_date TEXT,
            completion_date TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects (id),
            FOREIGN KEY (milestone_id) REFERENCES milestones (id)
        )
        ''')
        
        # Project templates table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS project_templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            template_data TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Project resources table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS project_resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            resource_type TEXT,
            resource_name TEXT,
            resource_url TEXT,
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects (id)
        )
        ''')
        
        # Project progress log
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
    
    def create_project(self, name: str, description: str = "", priority: int = 3, 
                      start_date: str = None, target_date: str = None) -> Dict[str, Any]:
        """Create a new project with comprehensive tracking"""
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
        
        return {
            "success": True,
            "project_id": project_id,
            "message": f"Project '{name}' created successfully"
        }
    
    def chart_project_course(self, project_id: int, milestones: List[Dict]) -> Dict[str, Any]:
        """Chart the complete course for a project with milestones and dependencies"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Verify project exists
        cursor.execute('SELECT name FROM projects WHERE id = ?', (project_id,))
        project = cursor.fetchone()
        if not project:
            conn.close()
            return {"success": False, "error": "Project not found"}
        
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
        
        return {
            "success": True,
            "milestone_ids": milestone_ids,
            "message": f"Course charted for project with {len(milestones)} milestones"
        }
    
    def get_project_status(self, project_id: int) -> Dict[str, Any]:
        """Get comprehensive project status with progress tracking"""
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
            return {"success": False, "error": "Project not found"}
        
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
        
        return {
            "success": True,
            "project": project_data,
            "milestones": milestones,
            "recent_progress": recent_progress,
            "metrics": {
                "total_milestones": total_milestones,
                "completed_milestones": completed_milestones,
                "progress_percentage": round(progress_percentage, 2)
            }
        }
    
    def schedule_project_reminders(self, project_id: int, reminder_settings: Dict) -> Dict[str, Any]:
        """Schedule automated project reminders and check-ins"""
        # This would integrate with calendar systems or notification services
        # For now, we'll log the reminder settings
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
        
        return {
            "success": True,
            "message": "Project reminders scheduled successfully"
        }
    
    def update_project_progress(self, project_id: int, milestone_id: int = None, 
                              status: str = None, notes: str = "") -> Dict[str, Any]:
        """Update project or milestone progress with detailed logging"""
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
        
        return {
            "success": True,
            "message": "Progress updated successfully"
        }
    
    def get_all_projects_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive dashboard view of all projects"""
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
        
        # Get projects needing attention (overdue, high priority, etc.)
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
        
        return {
            "success": True,
            "projects": projects,
            "attention_needed": attention_needed,
            "summary": {
                "total_projects": len(projects),
                "active_projects": len([p for p in projects if p['status'] in ['active', 'in_progress']]),
                "completed_projects": len([p for p in projects if p['status'] == 'completed'])
            }
        }

async def handle_request():
    """Handle incoming JSON-RPC requests using proven async pattern"""
    pm = ProjectManagementMCP()
    
    while True:
        try:
            # Use the proven async stdin reading pattern
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
            
            request = json.loads(line.strip())
            request_id = request.get("id")
            
            if request.get("method") == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "project-management-mcp",
                            "version": "1.0.0"
                        }
                    }
                }
                
            elif request.get("method") == "tools/list":
                response = {
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
                
            elif request.get("method") == "resources/list":
                # Add missing resources/list method
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "resources": []
                    }
                }
                
            elif request.get("method") == "tools/call":
                tool_name = request["params"]["name"]
                tool_args = request["params"].get("arguments", {})
                
                try:
                    if tool_name == "create_project":
                        result = pm.create_project(**tool_args)
                    elif tool_name == "chart_project_course":
                        result = pm.chart_project_course(**tool_args)
                    elif tool_name == "get_project_status":
                        result = pm.get_project_status(**tool_args)
                    elif tool_name == "schedule_project_reminders":
                        result = pm.schedule_project_reminders(**tool_args)
                    elif tool_name == "update_project_progress":
                        result = pm.update_project_progress(**tool_args)
                    elif tool_name == "get_all_projects_dashboard":
                        result = pm.get_all_projects_dashboard()
                    else:
                        result = {"error": f"Unknown tool: {tool_name}"}
                    
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps(result, indent=2)
                                }
                            ]
                        }
                    }
                except Exception as e:
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32603,
                            "message": f"Internal error: {str(e)}"
                        }
                    }
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {request.get('method')}"
                    }
                }
            
            print(json.dumps(response))
            sys.stdout.flush()
            
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": request.get("id") if 'request' in locals() else None,
                "error": {
                    "code": -32700,
                    "message": f"Parse error: {str(e)}"
                }
            }
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == "__main__":
    asyncio.run(handle_request())
