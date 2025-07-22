#!/usr/bin/env python3
"""
DuckDB Analytics MCP Server - Protocol Fixed
Revolutionary Business Intelligence with proper JSON-RPC implementation
Fixed to match working MCP server patterns exactly
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional, Union
import argparse
from pathlib import Path
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    import duckdb
    logger.info("DuckDB imported successfully")
except ImportError:
    logger.info("Installing DuckDB...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "duckdb"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    import duckdb
    logger.info("DuckDB installed successfully")

class DuckDBAnalyticsServer:
    """High-performance analytics server using DuckDB for business intelligence"""
    
    def __init__(self, db_path: str = ":memory:", readonly: bool = False):
        self.db_path = db_path
        self.readonly = readonly
        self.connection = None
        self._init_database()
        self._setup_analytics_environment()
    
    def _init_database(self):
        """Initialize DuckDB connection with analytics optimization"""
        try:
            if self.db_path == ":memory:":
                self.connection = duckdb.connect(":memory:")
                logger.info("Connected to in-memory DuckDB database")
            else:
                db_dir = Path(self.db_path).parent
                db_dir.mkdir(parents=True, exist_ok=True)
                self.connection = duckdb.connect(self.db_path, read_only=self.readonly)
                logger.info(f"Connected to DuckDB database: {self.db_path}")
            
            # Configure for analytics performance
            self.connection.execute("SET memory_limit='1GB'")
            self.connection.execute("SET threads=4")
            
        except Exception as e:
            logger.error(f"Failed to initialize DuckDB: {e}")
            raise
    
    def _setup_analytics_environment(self):
        """Set up analytics functions and sample data structure"""
        try:
            self.connection.execute("CREATE SCHEMA IF NOT EXISTS analytics")
            
            # Business metrics table
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS analytics.business_metrics (
                    date DATE,
                    metric_name VARCHAR,
                    metric_value DOUBLE,
                    category VARCHAR,
                    subcategory VARCHAR,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Project analytics table
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS analytics.project_metrics (
                    project_name VARCHAR,
                    task_type VARCHAR,
                    duration_minutes DOUBLE,
                    automation_level DOUBLE,
                    efficiency_score DOUBLE,
                    date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            logger.info("Analytics environment setup complete")
            
        except Exception as e:
            logger.error(f"Failed to setup analytics environment: {e}")
    
    async def execute_query(self, query: str) -> Dict[str, Any]:
        """Execute SQL query with comprehensive error handling"""
        try:
            if self.readonly:
                query_upper = query.upper().strip()
                if any(keyword in query_upper for keyword in ['INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER']):
                    return {
                        "success": False,
                        "error": "Write operations not allowed in readonly mode"
                    }
            
            result = self.connection.execute(query).fetchall()
            columns = [desc[0] for desc in self.connection.description] if self.connection.description else []
            
            rows = []
            for row in result:
                row_dict = {}
                for i, value in enumerate(row):
                    column_name = columns[i] if i < len(columns) else f"column_{i}"
                    if isinstance(value, (int, float, str, bool, type(None))):
                        row_dict[column_name] = value
                    else:
                        row_dict[column_name] = str(value)
                rows.append(row_dict)
            
            return {
                "success": True,
                "columns": columns,
                "rows": rows,
                "row_count": len(rows)
            }
            
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def load_csv_data(self, file_path: str, table_name: str, schema: str = "analytics") -> Dict[str, Any]:
        """Load CSV data into DuckDB table for analysis"""
        try:
            full_table_name = f"{schema}.{table_name}"
            
            query = f"""
                CREATE OR REPLACE TABLE {full_table_name} AS 
                SELECT * FROM read_csv_auto('{file_path}')
            """
            
            await self.execute_query(query)
            
            count_query = f"SELECT COUNT(*) as total_rows FROM {full_table_name}"
            count_result = await self.execute_query(count_query)
            row_count = count_result["rows"][0]["total_rows"] if count_result["success"] else 0
            
            return {
                "success": True,
                "table_name": full_table_name,
                "row_count": row_count
            }
            
        except Exception as e:
            logger.error(f"CSV loading failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def analyze_business_performance(self) -> Dict[str, Any]:
        """Generate comprehensive business performance analytics"""
        try:
            analyses = {}
            
            # Check if tables have data
            metrics_count = await self.execute_query("SELECT COUNT(*) as count FROM analytics.business_metrics")
            project_count = await self.execute_query("SELECT COUNT(*) as count FROM analytics.project_metrics")
            
            if metrics_count["success"] and metrics_count["rows"][0]["count"] > 0:
                trend_query = """
                    SELECT 
                        category,
                        COUNT(*) as metric_count,
                        AVG(metric_value) as avg_value,
                        MIN(metric_value) as min_value,
                        MAX(metric_value) as max_value
                    FROM analytics.business_metrics 
                    GROUP BY category
                    ORDER BY avg_value DESC
                """
                analyses["business_trends"] = await self.execute_query(trend_query)
            
            if project_count["success"] and project_count["rows"][0]["count"] > 0:
                efficiency_query = """
                    SELECT 
                        project_name,
                        AVG(automation_level) as avg_automation,
                        AVG(efficiency_score) as avg_efficiency,
                        COUNT(*) as task_count
                    FROM analytics.project_metrics 
                    GROUP BY project_name
                    ORDER BY avg_efficiency DESC
                """
                analyses["project_efficiency"] = await self.execute_query(efficiency_query)
            
            return {
                "success": True,
                "analyses": analyses,
                "has_data": len(analyses) > 0
            }
            
        except Exception as e:
            logger.error(f"Business analysis failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

class MCPServer:
    """MCP Protocol Handler - Fixed to match working servers exactly"""
    
    def __init__(self, db_path: str = ":memory:", readonly: bool = False):
        self.analytics_server = DuckDBAnalyticsServer(db_path, readonly)
    
    def get_request_id(self, request):
        """Handle request ID with proper null handling like working servers"""
        req_id = request.get("id")
        if req_id is None:
            return 0
        return req_id
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP requests with exact protocol matching working servers"""
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
                        "serverInfo": {"name": "duckdb-analytics-server", "version": "1.0.0"}
                    }
                }
            
            elif method == "tools/list":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "tools": [
                            {
                                "name": "execute_query",
                                "description": "Execute SQL query on DuckDB database for advanced analytics",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "query": {
                                            "type": "string",
                                            "description": "SQL query to execute"
                                        }
                                    },
                                    "required": ["query"]
                                }
                            },
                            {
                                "name": "load_csv_data",
                                "description": "Load CSV file data into DuckDB table for analysis",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "file_path": {
                                            "type": "string",
                                            "description": "Path to CSV file"
                                        },
                                        "table_name": {
                                            "type": "string",
                                            "description": "Name for the table to create"
                                        }
                                    },
                                    "required": ["file_path", "table_name"]
                                }
                            },
                            {
                                "name": "analyze_business_performance",
                                "description": "Generate comprehensive business performance analytics report",
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
                
                if tool_name == "execute_query":
                    result = await self.analytics_server.execute_query(arguments.get("query", ""))
                elif tool_name == "load_csv_data":
                    result = await self.analytics_server.load_csv_data(
                        arguments.get("file_path", ""),
                        arguments.get("table_name", "")
                    )
                elif tool_name == "analyze_business_performance":
                    result = await self.analytics_server.analyze_business_performance()
                else:
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {"code": -32602, "message": f"Unknown tool: {tool_name}"}
                    }
                
                response_text = json.dumps(result, indent=2, default=str)
                
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"content": [{"type": "text", "text": response_text}]}
                }
            
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": f"Method not found: {method}"}
                }
        
        except Exception as e:
            logger.error(f"Error handling request: {str(e)}")
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
            }

async def main():
    """Main loop exactly matching working MCP servers"""
    parser = argparse.ArgumentParser(description="DuckDB Analytics MCP Server")
    parser.add_argument("--db-path", default=":memory:", help="Path to DuckDB database file")
    parser.add_argument("--readonly", action="store_true", help="Run in readonly mode")
    args = parser.parse_args()
    
    logger.info("DuckDB Analytics MCP Server starting...")
    logger.info(f"Database: {args.db_path}")
    
    server = MCPServer(args.db_path, args.readonly)
    
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
                
            request = json.loads(line.strip())
            response = await server.handle_request(request)
            
            print(json.dumps(response))
            sys.stdout.flush()
            
        except json.JSONDecodeError:
            continue
        except Exception as e:
            continue

if __name__ == "__main__":
    asyncio.run(main())
