#!/usr/bin/env python3
"""
DuckDB Analytics MCP Server for Revolutionary Business Intelligence
Integrates high-performance analytics with Ruben's 9-server MCP ecosystem
Amplifies business optimization with real data processing capabilities
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional, Union
import argparse
from pathlib import Path
import tempfile
import subprocess

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    import duckdb
    logger.info("DuckDB imported successfully")
except ImportError:
    logger.error("DuckDB not installed. Installing...")
    # Suppress pip output to prevent JSON protocol interference
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "duckdb"], 
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL
    )
    import duckdb
    logger.info("DuckDB installed and imported successfully")

class DuckDBAnalyticsServer:
    """High-performance analytics server using DuckDB for business intelligence"""
    
    def __init__(self, db_path: str = ":memory:", readonly: bool = False):
        self.db_path = db_path
        self.readonly = readonly
        self.connection = None
        
        # Initialize database
        self._init_database()
        
        # Set up analytics capabilities
        self._setup_analytics_environment()
    
    def _init_database(self):
        """Initialize DuckDB connection with analytics optimization"""
        try:
            if self.db_path == ":memory:":
                self.connection = duckdb.connect(":memory:")
                logger.info("Connected to in-memory DuckDB database")
            else:
                # Ensure directory exists
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
            # Create analytics schema
            self.connection.execute("CREATE SCHEMA IF NOT EXISTS analytics")
            
            # Sample business metrics table structure
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
            
            # Sample project analytics table
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
            
            # Sample workflow analytics table
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS analytics.workflow_analytics (
                    workflow_name VARCHAR,
                    step_name VARCHAR,
                    execution_time DOUBLE,
                    success_rate DOUBLE,
                    error_count INTEGER,
                    optimization_opportunity DOUBLE,
                    date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            logger.info("Analytics environment setup complete")
            
        except Exception as e:
            logger.error(f"Failed to setup analytics environment: {e}")
    
    async def execute_query(self, query: str) -> Dict[str, Any]:
        """Execute SQL query with comprehensive error handling and optimization"""
        try:
            logger.info(f"Executing query: {query[:100]}...")
            
            # Security check for readonly mode
            if self.readonly:
                query_upper = query.upper().strip()
                if any(keyword in query_upper for keyword in ['INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER']):
                    return {
                        "success": False,
                        "error": "Write operations not allowed in readonly mode",
                        "query": query
                    }
            
            # Execute query
            result = self.connection.execute(query).fetchall()
            columns = [desc[0] for desc in self.connection.description] if self.connection.description else []
            
            # Format results
            rows = []
            for row in result:
                row_dict = {}
                for i, value in enumerate(row):
                    column_name = columns[i] if i < len(columns) else f"column_{i}"
                    # Handle various data types
                    if isinstance(value, (int, float, str, bool)):
                        row_dict[column_name] = value
                    else:
                        row_dict[column_name] = str(value)
                rows.append(row_dict)
            
            return {
                "success": True,
                "columns": columns,
                "rows": rows,
                "row_count": len(rows),
                "query": query
            }
            
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "query": query
            }
    
    async def load_csv_data(self, file_path: str, table_name: str, schema: str = "analytics") -> Dict[str, Any]:
        """Load CSV data into DuckDB table for analysis"""
        try:
            full_table_name = f"{schema}.{table_name}"
            
            # Auto-detect and create table from CSV
            query = f"""
                CREATE OR REPLACE TABLE {full_table_name} AS 
                SELECT * FROM read_csv_auto('{file_path}')
            """
            
            await self.execute_query(query)
            
            # Get table info
            info_query = f"DESCRIBE {full_table_name}"
            table_info = await self.execute_query(info_query)
            
            # Get row count
            count_query = f"SELECT COUNT(*) as total_rows FROM {full_table_name}"
            count_result = await self.execute_query(count_query)
            row_count = count_result["rows"][0]["total_rows"] if count_result["success"] else 0
            
            return {
                "success": True,
                "table_name": full_table_name,
                "file_path": file_path,
                "row_count": row_count,
                "schema": table_info["rows"] if table_info["success"] else []
            }
            
        except Exception as e:
            logger.error(f"CSV loading failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "file_path": file_path,
                "table_name": table_name
            }
    
    async def analyze_business_performance(self) -> Dict[str, Any]:
        """Generate comprehensive business performance analytics"""
        try:
            analyses = {}
            
            # Business metrics trend analysis
            trend_query = """
                SELECT 
                    category,
                    COUNT(*) as metric_count,
                    AVG(metric_value) as avg_value,
                    MIN(metric_value) as min_value,
                    MAX(metric_value) as max_value,
                    STDDEV(metric_value) as std_deviation
                FROM analytics.business_metrics 
                GROUP BY category
                ORDER BY avg_value DESC
            """
            analyses["business_trends"] = await self.execute_query(trend_query)
            
            # Project efficiency analysis
            efficiency_query = """
                SELECT 
                    project_name,
                    AVG(automation_level) as avg_automation,
                    AVG(efficiency_score) as avg_efficiency,
                    SUM(duration_minutes) as total_duration,
                    COUNT(*) as task_count
                FROM analytics.project_metrics 
                GROUP BY project_name
                ORDER BY avg_efficiency DESC
            """
            analyses["project_efficiency"] = await self.execute_query(efficiency_query)
            
            # Workflow optimization opportunities
            optimization_query = """
                SELECT 
                    workflow_name,
                    AVG(execution_time) as avg_execution_time,
                    AVG(success_rate) as avg_success_rate,
                    SUM(error_count) as total_errors,
                    AVG(optimization_opportunity) as optimization_potential
                FROM analytics.workflow_analytics 
                GROUP BY workflow_name
                ORDER BY optimization_potential DESC
            """
            analyses["optimization_opportunities"] = await self.execute_query(optimization_query)
            
            return {
                "success": True,
                "analyses": analyses,
                "generated_at": self.connection.execute("SELECT CURRENT_TIMESTAMP").fetchone()[0]
            }
            
        except Exception as e:
            logger.error(f"Business analysis failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_table_info(self, schema: str = "analytics") -> Dict[str, Any]:
        """Get comprehensive database schema information"""
        try:
            # Get all tables in schema
            tables_query = f"""
                SELECT table_name, table_type 
                FROM information_schema.tables 
                WHERE table_schema = '{schema}'
                ORDER BY table_name
            """
            tables_result = await self.execute_query(tables_query)
            
            # Get detailed info for each table
            table_details = {}
            if tables_result["success"]:
                for table_row in tables_result["rows"]:
                    table_name = table_row["table_name"]
                    full_name = f"{schema}.{table_name}"
                    
                    # Column information
                    columns_query = f"DESCRIBE {full_name}"
                    columns_result = await self.execute_query(columns_query)
                    
                    # Row count
                    count_query = f"SELECT COUNT(*) as row_count FROM {full_name}"
                    count_result = await self.execute_query(count_query)
                    row_count = count_result["rows"][0]["row_count"] if count_result["success"] else 0
                    
                    table_details[table_name] = {
                        "columns": columns_result["rows"] if columns_result["success"] else [],
                        "row_count": row_count,
                        "table_type": table_row["table_type"]
                    }
            
            return {
                "success": True,
                "schema": schema,
                "tables": table_details
            }
            
        except Exception as e:
            logger.error(f"Schema inspection failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "schema": schema
            }

class MCPServer:
    """MCP Protocol Handler for DuckDB Analytics Server"""
    
    def __init__(self, db_path: str = ":memory:", readonly: bool = False):
        self.analytics_server = DuckDBAnalyticsServer(db_path, readonly)
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP protocol requests"""
        try:
            method = request.get("method")
            params = request.get("params", {})
            
            if method == "initialize":
                return {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "duckdb-analytics-server",
                        "version": "1.0.0"
                    }
                }
            
            elif method == "tools/list":
                return {
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
                                    },
                                    "schema": {
                                        "type": "string",
                                        "description": "Database schema name (default: analytics)",
                                        "default": "analytics"
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
                        },
                        {
                            "name": "get_table_info",
                            "description": "Get database schema and table information",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "schema": {
                                        "type": "string",
                                        "description": "Database schema name (default: analytics)",
                                        "default": "analytics"
                                    }
                                },
                                "required": []
                            }
                        }
                    ]
                }
            
            elif method == "tools/call":
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})
                
                if tool_name == "execute_query":
                    result = await self.analytics_server.execute_query(tool_args.get("query"))
                elif tool_name == "load_csv_data":
                    result = await self.analytics_server.load_csv_data(
                        tool_args.get("file_path"),
                        tool_args.get("table_name"),
                        tool_args.get("schema", "analytics")
                    )
                elif tool_name == "analyze_business_performance":
                    result = await self.analytics_server.analyze_business_performance()
                elif tool_name == "get_table_info":
                    result = await self.analytics_server.get_table_info(
                        tool_args.get("schema", "analytics")
                    )
                else:
                    return {"error": f"Unknown tool: {tool_name}"}
                
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2, default=str)
                        }
                    ]
                }
            
            else:
                return {"error": f"Unknown method: {method}"}
                
        except Exception as e:
            logger.error(f"Request handling failed: {e}")
            return {"error": str(e)}

async def main():
    """Main server entry point"""
    parser = argparse.ArgumentParser(description="DuckDB Analytics MCP Server")
    parser.add_argument("--db-path", default=":memory:", help="Path to DuckDB database file")
    parser.add_argument("--readonly", action="store_true", help="Run in readonly mode")
    args = parser.parse_args()
    
    logger.info(f"Starting DuckDB Analytics MCP Server")
    logger.info(f"Database: {args.db_path}")
    logger.info(f"Readonly: {args.readonly}")
    
    server = MCPServer(args.db_path, args.readonly)
    
    # MCP protocol communication loop
    while True:
        try:
            # Read from stdin
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
            
            # Parse request
            request = json.loads(line.strip())
            
            # Handle request
            response = await server.handle_request(request)
            
            # Send response
            response_json = json.dumps(response)
            print(response_json, flush=True)
            
        except json.JSONDecodeError:
            logger.warning("Invalid JSON received")
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            error_response = {"error": str(e)}
            print(json.dumps(error_response), flush=True)

if __name__ == "__main__":
    asyncio.run(main())
