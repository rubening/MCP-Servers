#!/usr/bin/env python3
"""
Personal Knowledge Intelligence MCP Server - Protocol Fixed
The Ultimate "Passive Buff" System with proper JSON-RPC implementation
Fixed to match working MCP server patterns exactly
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
from datetime import datetime, date
import hashlib
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    import duckdb
    logger.info("DuckDB imported successfully")
except ImportError:
    logger.info("DuckDB not available - using basic storage")
    duckdb = None

class PersonalKnowledgeIntelligence:
    """Revolutionary Personal Knowledge Intelligence Engine - The Ultimate Passive Buff System"""
    
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.connection = None
        self.insights_storage = []  # Fallback storage
        
        if duckdb:
            self._init_knowledge_database()
        else:
            logger.info("Using basic in-memory storage")
    
    def _init_knowledge_database(self):
        """Initialize DuckDB connection optimized for knowledge intelligence"""
        try:
            if self.db_path == ":memory:":
                self.connection = duckdb.connect(":memory:")
                logger.info("Connected to in-memory knowledge database")
            else:
                # Ensure directory exists
                db_dir = Path(self.db_path).parent
                db_dir.mkdir(parents=True, exist_ok=True)
                
                self.connection = duckdb.connect(self.db_path)
                logger.info(f"Connected to knowledge database: {self.db_path}")
            
            # Create simple insights table
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS conversation_insights (
                    insight_id VARCHAR PRIMARY KEY,
                    conversation_date DATE,
                    conversation_topic VARCHAR,
                    insight_content TEXT,
                    key_concepts TEXT,
                    cognitive_score DOUBLE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            logger.info("Knowledge intelligence database setup complete")
            
        except Exception as e:
            logger.error(f"Failed to initialize knowledge database: {e}")
            self.connection = None
    
    def _generate_insight_id(self, content: str) -> str:
        """Generate unique insight identifier"""
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        return f"insight_{datetime.now().strftime('%Y%m%d')}_{content_hash}"
    
    def _extract_key_concepts(self, content: str) -> List[str]:
        """Extract key concepts using pattern recognition"""
        concepts = []
        
        # Technical terms
        tech_patterns = re.findall(r'\b(?:MCP|API|server|database|tool|automation|integration)\b', content, re.IGNORECASE)
        concepts.extend([term.lower() for term in tech_patterns])
        
        # Cognitive terms
        cognitive_patterns = re.findall(r'\b(?:pattern|insight|framework|organization|efficiency)\b', content, re.IGNORECASE)
        concepts.extend([term.lower() for term in cognitive_patterns])
        
        return list(set(concepts))[:5]
    
    def _calculate_cognitive_score(self, content: str) -> float:
        """Calculate cognitive enhancement score"""
        content_lower = content.lower()
        indicators = ['pattern', 'insight', 'systematic', 'framework', 'efficiency', 'optimization']
        score = sum(1 for indicator in indicators if indicator in content_lower) / len(indicators)
        return min(1.0, score)
    
    async def capture_insights(self, conversation_content: str, topic: str = "general") -> Dict[str, Any]:
        """PASSIVE BUFF: Automatically capture insights from conversation"""
        try:
            current_date = date.today()
            insight_id = self._generate_insight_id(conversation_content)
            key_concepts = self._extract_key_concepts(conversation_content)
            cognitive_score = self._calculate_cognitive_score(conversation_content)
            
            insight_data = {
                "insight_id": insight_id,
                "conversation_date": current_date,
                "conversation_topic": topic,
                "insight_content": conversation_content,
                "key_concepts": key_concepts,
                "cognitive_score": cognitive_score
            }
            
            # Store insight
            if self.connection:
                try:
                    self.connection.execute("""
                        INSERT INTO conversation_insights 
                        (insight_id, conversation_date, conversation_topic, insight_content, key_concepts, cognitive_score)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, [insight_id, current_date, topic, conversation_content, 
                          ", ".join(key_concepts), cognitive_score])
                except Exception as e:
                    logger.error(f"Database insert failed: {e}")
                    self.insights_storage.append(insight_data)
            else:
                self.insights_storage.append(insight_data)
            
            return {
                "success": True,
                "insight_id": insight_id,
                "key_concepts": key_concepts,
                "cognitive_score": cognitive_score,
                "passive_buff_enhancement": cognitive_score * 1.2
            }
            
        except Exception as e:
            logger.error(f"Insight capture failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def search_insights(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search captured insights"""
        try:
            results = []
            
            if self.connection:
                try:
                    cursor = self.connection.execute("""
                        SELECT insight_id, conversation_topic, insight_content, cognitive_score
                        FROM conversation_insights 
                        WHERE insight_content LIKE ? 
                        ORDER BY cognitive_score DESC 
                        LIMIT ?
                    """, [f"%{query}%", limit])
                    
                    for row in cursor.fetchall():
                        results.append({
                            "insight_id": row[0],
                            "topic": row[1], 
                            "content": row[2][:200] + "...",
                            "score": row[3]
                        })
                except Exception as e:
                    logger.error(f"Database search failed: {e}")
            
            # Fallback to in-memory search
            if not results and self.insights_storage:
                for insight in self.insights_storage:
                    if query.lower() in insight["insight_content"].lower():
                        results.append({
                            "insight_id": insight["insight_id"],
                            "topic": insight["conversation_topic"],
                            "content": insight["insight_content"][:200] + "...",
                            "score": insight["cognitive_score"]
                        })
                        if len(results) >= limit:
                            break
            
            return {
                "success": True,
                "query": query,
                "results": results,
                "total_found": len(results)
            }
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

class MCPServer:
    """MCP Protocol Handler - Fixed to match working servers exactly"""
    
    def __init__(self, db_path: str = ":memory:"):
        self.knowledge_intelligence = PersonalKnowledgeIntelligence(db_path)
    
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
                        "serverInfo": {"name": "personal-knowledge-intelligence", "version": "1.0.0"}
                    }
                }
            
            elif method == "tools/list":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "tools": [
                            {
                                "name": "capture_conversation_insights",
                                "description": "PASSIVE BUFF: Automatically capture and analyze conversation insights for enhanced learning",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "conversation_content": {
                                            "type": "string",
                                            "description": "The conversation content to analyze and capture insights from"
                                        },
                                        "topic": {
                                            "type": "string",
                                            "description": "The conversation topic/category (default: general)"
                                        }
                                    },
                                    "required": ["conversation_content"]
                                }
                            },
                            {
                                "name": "search_knowledge_base",
                                "description": "Search captured insights with relevance scoring",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "query": {
                                            "type": "string",
                                            "description": "Search query to find relevant insights"
                                        },
                                        "limit": {
                                            "type": "integer",
                                            "description": "Maximum number of results to return (default: 10)"
                                        }
                                    },
                                    "required": ["query"]
                                }
                            }
                        ]
                    }
                }
            
            elif method == "tools/call":
                params = request.get("params", {})
                tool_name = params.get("name", "")
                arguments = params.get("arguments", {})
                
                if tool_name == "capture_conversation_insights":
                    result = await self.knowledge_intelligence.capture_insights(
                        arguments.get("conversation_content", ""),
                        arguments.get("topic", "general")
                    )
                elif tool_name == "search_knowledge_base":
                    result = await self.knowledge_intelligence.search_insights(
                        arguments.get("query", ""),
                        arguments.get("limit", 10)
                    )
                else:
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {"code": -32602, "message": f"Unknown tool: {tool_name}"}
                    }
                
                # Format response exactly like working servers
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
    import argparse
    
    parser = argparse.ArgumentParser(description="Personal Knowledge Intelligence MCP Server")
    parser.add_argument("--db-path", default=":memory:", help="Path to knowledge database file")
    args = parser.parse_args()
    
    logger.info("Personal Knowledge Intelligence MCP Server starting...")
    logger.info(f"Knowledge Database: {args.db_path}")
    
    server = MCPServer(args.db_path)
    
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
            # Silent continue like working servers
            continue
        except Exception as e:
            # Silent continue like working servers
            continue

if __name__ == "__main__":
    asyncio.run(main())
