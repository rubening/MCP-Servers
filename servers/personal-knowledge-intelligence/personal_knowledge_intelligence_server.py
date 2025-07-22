#!/usr/bin/env python3
"""
Personal Knowledge Intelligence MCP Server - The Ultimate "Passive Buff" System
Automatically captures, connects, and enhances conversation insights for exponential learning
Integrates with DuckDB Analytics for high-performance knowledge management

This system transforms every Claude conversation into captured knowledge assets,
providing Si PoLR support through external knowledge organization and
Ni amplification through automated pattern recognition and connection mapping.
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
from datetime import datetime, date
import hashlib
import re

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
    subprocess.check_call([sys.executable, "-m", "pip", "install", "duckdb"])
    import duckdb
    logger.info("DuckDB installed and imported successfully")

class PersonalKnowledgeIntelligence:
    """Revolutionary Personal Knowledge Intelligence Engine - The Ultimate Passive Buff System"""
    
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.connection = None
        
        # Initialize knowledge database
        self._init_knowledge_database()
        
        # Set up knowledge capture and analytics
        self._setup_knowledge_environment()
    
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
            
            # Configure for optimal knowledge processing
            self.connection.execute("SET memory_limit='2GB'")
            self.connection.execute("SET threads=4")
            
        except Exception as e:
            logger.error(f"Failed to initialize knowledge database: {e}")
            raise
    
    def _setup_knowledge_environment(self):
        """Set up knowledge intelligence tables and functions"""
        try:
            # Create knowledge schema
            self.connection.execute("CREATE SCHEMA IF NOT EXISTS knowledge")
            
            # Conversation insights table - The core passive buff system
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS knowledge.conversation_insights (
                    insight_id VARCHAR PRIMARY KEY,
                    conversation_date DATE,
                    conversation_topic VARCHAR,
                    insight_type VARCHAR,
                    insight_content TEXT,
                    key_concepts ARRAY(VARCHAR),
                    pattern_connections ARRAY(VARCHAR),
                    learning_efficiency DOUBLE,
                    synthesis_quality DOUBLE,
                    ni_pattern_recognition BOOLEAN,
                    ti_framework_building BOOLEAN,
                    se_action_orientation BOOLEAN,
                    fi_value_alignment BOOLEAN,
                    cognitive_enhancement_score DOUBLE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Knowledge connections table - Pattern mapping system
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS knowledge.knowledge_connections (
                    connection_id VARCHAR PRIMARY KEY,
                    source_insight_id VARCHAR,
                    target_insight_id VARCHAR,
                    connection_type VARCHAR,
                    connection_strength DOUBLE,
                    pattern_category VARCHAR,
                    cross_domain_mapping BOOLEAN,
                    discovery_date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Learning analytics table - Performance tracking
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS knowledge.learning_analytics (
                    session_id VARCHAR PRIMARY KEY,
                    session_date DATE,
                    session_topic VARCHAR,
                    insight_count INTEGER,
                    pattern_recognition_rate DOUBLE,
                    knowledge_synthesis_score DOUBLE,
                    learning_velocity DOUBLE,
                    cognitive_efficiency DOUBLE,
                    breakthrough_moments INTEGER,
                    knowledge_assets_generated INTEGER,
                    passive_buff_enhancement DOUBLE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Knowledge assets table - Reusable intelligence
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS knowledge.knowledge_assets (
                    asset_id VARCHAR PRIMARY KEY,
                    asset_name VARCHAR,
                    asset_type VARCHAR,
                    asset_content TEXT,
                    source_insights ARRAY(VARCHAR),
                    reusability_score DOUBLE,
                    enhancement_value DOUBLE,
                    cross_project_applicability DOUBLE,
                    generated_date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Cognitive function optimization table - Stack-specific enhancement
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS knowledge.cognitive_optimization (
                    optimization_id VARCHAR PRIMARY KEY,
                    function_slot VARCHAR,
                    function_type VARCHAR,
                    optimization_strategy VARCHAR,
                    effectiveness_score DOUBLE,
                    si_polr_compensation BOOLEAN,
                    ni_pattern_amplification BOOLEAN,
                    ti_framework_satisfaction BOOLEAN,
                    fe_external_organization BOOLEAN,
                    implementation_date DATE,
                    success_metrics TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            logger.info("Knowledge intelligence environment setup complete")
            
        except Exception as e:
            logger.error(f"Failed to setup knowledge environment: {e}")
    
    def _generate_insight_id(self, content: str, timestamp: str) -> str:
        """Generate unique insight identifier"""
        content_hash = hashlib.md5(f"{content}{timestamp}".encode()).hexdigest()[:8]
        return f"insight_{datetime.now().strftime('%Y%m%d')}_{content_hash}"
    
    def _extract_key_concepts(self, content: str) -> List[str]:
        """Extract key concepts using pattern recognition"""
        # Advanced concept extraction - looks for technical terms, important patterns
        concepts = []
        
        # Technical terms (MCP, APIs, servers, etc.)
        tech_patterns = re.findall(r'\b[A-Z]{2,}(?:\s+[A-Z][a-z]*)*\b|(?:server|API|database|framework|system|tool|integration|automation|optimization)\b', content, re.IGNORECASE)
        concepts.extend([term.lower() for term in tech_patterns])
        
        # Cognitive function terms
        cognitive_patterns = re.findall(r'\b(?:Ni|Ne|Si|Se|Ti|Te|Fi|Fe|PoLR|seeking|valued|unconscious|pattern|insight|framework|organization|action)\b', content)
        concepts.extend([term.lower() for term in cognitive_patterns])
        
        # Business/productivity terms
        business_patterns = re.findall(r'\b(?:efficiency|productivity|automation|optimization|workflow|intelligence|analytics|enhancement|passive\s+buff|multiplicative)\b', content, re.IGNORECASE)
        concepts.extend([term.lower() for term in business_patterns])
        
        # Remove duplicates and return top concepts
        return list(set(concepts))[:10]
    
    def _detect_pattern_connections(self, content: str, existing_insights: List[str]) -> List[str]:
        """Detect connections to existing knowledge patterns"""
        connections = []
        
        # This would use more sophisticated pattern matching in production
        # For now, using keyword overlap detection
        content_words = set(content.lower().split())
        
        for insight in existing_insights[:20]:  # Check recent insights
            insight_words = set(insight.lower().split())
            overlap = len(content_words.intersection(insight_words))
            if overlap > 3:  # Threshold for connection
                connections.append(insight)
        
        return connections[:5]  # Return top 5 connections
    
    def _calculate_cognitive_scores(self, content: str) -> Dict[str, float]:
        """Calculate cognitive function enhancement scores"""
        content_lower = content.lower()
        
        # Pattern recognition indicators (Ni 2nd slot)
        ni_indicators = ['pattern', 'connection', 'insight', 'synthesis', 'framework', 'system']
        ni_score = sum(1 for indicator in ni_indicators if indicator in content_lower) / len(ni_indicators)
        
        # Logical framework building (Ti 4th slot seeking)
        ti_indicators = ['why', 'reason', 'logic', 'systematic', 'framework', 'structured']
        ti_score = sum(1 for indicator in ti_indicators if indicator in content_lower) / len(ti_indicators)
        
        # Action orientation (Se 3rd slot)
        se_indicators = ['implement', 'action', 'hands-on', 'immediate', 'practical', 'execute']
        se_score = sum(1 for indicator in se_indicators if indicator in content_lower) / len(se_indicators)
        
        # Value alignment (Fi 5th slot)
        fi_indicators = ['authentic', 'values', 'personal', 'meaningful', 'right', 'important']
        fi_score = sum(1 for indicator in fi_indicators if indicator in content_lower) / len(fi_indicators)
        
        # Overall cognitive enhancement
        cognitive_enhancement = (ni_score * 0.3 + ti_score * 0.3 + se_score * 0.25 + fi_score * 0.15)
        
        return {
            'ni_pattern_recognition': ni_score > 0.3,
            'ti_framework_building': ti_score > 0.3,
            'se_action_orientation': se_score > 0.3,
            'fi_value_alignment': fi_score > 0.2,
            'cognitive_enhancement_score': cognitive_enhancement
        }
    
    async def capture_conversation_insights(self, conversation_content: str, topic: str = "general") -> Dict[str, Any]:
        """PASSIVE BUFF: Automatically capture insights from conversation"""
        try:
            current_date = date.today()
            current_time = datetime.now().isoformat()
            
            # Generate unique insight ID
            insight_id = self._generate_insight_id(conversation_content, current_time)
            
            # Extract key concepts
            key_concepts = self._extract_key_concepts(conversation_content)
            
            # Get existing insights for connection detection
            existing_query = "SELECT insight_content FROM knowledge.conversation_insights ORDER BY created_at DESC LIMIT 50"
            existing_result = await self._execute_query(existing_query)
            existing_insights = [row['insight_content'] for row in existing_result.get('rows', [])]
            
            # Detect pattern connections
            pattern_connections = self._detect_pattern_connections(conversation_content, existing_insights)
            
            # Calculate cognitive enhancement scores
            cognitive_scores = self._calculate_cognitive_scores(conversation_content)
            
            # Determine insight type based on content analysis
            insight_type = "breakthrough" if any(word in conversation_content.lower() for word in ['revolutionary', 'breakthrough', 'game-changing', 'perfect']) else "incremental"
            
            # Calculate learning efficiency and synthesis quality
            learning_efficiency = min(1.0, len(key_concepts) / 10.0)  # Normalized concept density
            synthesis_quality = min(1.0, len(pattern_connections) / 5.0)  # Connection density
            
            # Insert insight into database
            insert_query = """
                INSERT INTO knowledge.conversation_insights (
                    insight_id, conversation_date, conversation_topic, insight_type,
                    insight_content, key_concepts, pattern_connections,
                    learning_efficiency, synthesis_quality,
                    ni_pattern_recognition, ti_framework_building, 
                    se_action_orientation, fi_value_alignment,
                    cognitive_enhancement_score
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            await self._execute_query(insert_query, [
                insight_id, current_date, topic, insight_type,
                conversation_content, key_concepts, pattern_connections,
                learning_efficiency, synthesis_quality,
                cognitive_scores['ni_pattern_recognition'],
                cognitive_scores['ti_framework_building'],
                cognitive_scores['se_action_orientation'],
                cognitive_scores['fi_value_alignment'],
                cognitive_scores['cognitive_enhancement_score']
            ])
            
            # Calculate passive buff enhancement value
            passive_buff_value = cognitive_scores['cognitive_enhancement_score'] * (1 + len(pattern_connections) * 0.1)
            
            return {
                "success": True,
                "insight_id": insight_id,
                "key_concepts": key_concepts,
                "pattern_connections": len(pattern_connections),
                "cognitive_enhancement_score": cognitive_scores['cognitive_enhancement_score'],
                "passive_buff_enhancement": passive_buff_value,
                "learning_efficiency": learning_efficiency,
                "synthesis_quality": synthesis_quality,
                "insight_type": insight_type
            }
            
        except Exception as e:
            logger.error(f"Insight capture failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def search_knowledge_base(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Intelligent search across captured knowledge with pattern matching"""
        try:
            # Advanced search using DuckDB full-text capabilities
            search_query = """
                SELECT 
                    insight_id,
                    conversation_topic,
                    insight_type,
                    insight_content,
                    key_concepts,
                    cognitive_enhancement_score,
                    created_at
                FROM knowledge.conversation_insights
                WHERE insight_content ILIKE ? 
                   OR array_to_string(key_concepts, ' ') ILIKE ?
                   OR conversation_topic ILIKE ?
                ORDER BY cognitive_enhancement_score DESC, created_at DESC
                LIMIT ?
            """
            
            search_pattern = f"%{query}%"
            result = await self._execute_query(search_query, [search_pattern, search_pattern, search_pattern, limit])
            
            if result["success"]:
                # Enhance results with relevance scoring
                enhanced_results = []
                for row in result["rows"]:
                    # Calculate relevance score
                    content_matches = row["insight_content"].lower().count(query.lower())
                    concept_matches = sum(1 for concept in row["key_concepts"] if query.lower() in concept.lower())
                    relevance_score = content_matches + (concept_matches * 2)
                    
                    enhanced_results.append({
                        **row,
                        "relevance_score": relevance_score
                    })
                
                # Sort by relevance
                enhanced_results.sort(key=lambda x: x["relevance_score"], reverse=True)
                
                return {
                    "success": True,
                    "query": query,
                    "results": enhanced_results,
                    "total_found": len(enhanced_results)
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"Knowledge search failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "query": query
            }
    
    async def analyze_learning_patterns(self, days: int = 30) -> Dict[str, Any]:
        """Generate comprehensive learning analytics and optimization insights"""
        try:
            # Learning velocity analysis
            velocity_query = """
                SELECT 
                    conversation_date,
                    COUNT(*) as daily_insights,
                    AVG(cognitive_enhancement_score) as avg_enhancement,
                    AVG(learning_efficiency) as avg_efficiency,
                    SUM(CASE WHEN insight_type = 'breakthrough' THEN 1 ELSE 0 END) as breakthroughs
                FROM knowledge.conversation_insights
                WHERE conversation_date >= CURRENT_DATE - INTERVAL ? DAYS
                GROUP BY conversation_date
                ORDER BY conversation_date DESC
            """
            
            velocity_result = await self._execute_query(velocity_query, [days])
            
            # Pattern recognition trends
            pattern_query = """
                SELECT 
                    conversation_topic,
                    COUNT(*) as insight_count,
                    AVG(cognitive_enhancement_score) as avg_enhancement,
                    SUM(CASE WHEN ni_pattern_recognition THEN 1 ELSE 0 END) as ni_activations,
                    SUM(CASE WHEN ti_framework_building THEN 1 ELSE 0 END) as ti_activations
                FROM knowledge.conversation_insights
                WHERE conversation_date >= CURRENT_DATE - INTERVAL ? DAYS
                GROUP BY conversation_topic
                ORDER BY avg_enhancement DESC
            """
            
            pattern_result = await self._execute_query(pattern_query, [days])
            
            # Cognitive function optimization analysis
            cognitive_query = """
                SELECT 
                    AVG(CASE WHEN ni_pattern_recognition THEN cognitive_enhancement_score ELSE 0 END) as ni_effectiveness,
                    AVG(CASE WHEN ti_framework_building THEN cognitive_enhancement_score ELSE 0 END) as ti_effectiveness,
                    AVG(CASE WHEN se_action_orientation THEN cognitive_enhancement_score ELSE 0 END) as se_effectiveness,
                    AVG(CASE WHEN fi_value_alignment THEN cognitive_enhancement_score ELSE 0 END) as fi_effectiveness,
                    COUNT(*) as total_insights
                FROM knowledge.conversation_insights
                WHERE conversation_date >= CURRENT_DATE - INTERVAL ? DAYS
            """
            
            cognitive_result = await self._execute_query(cognitive_query, [days])
            
            # Calculate passive buff statistics
            passive_buff_query = """
                SELECT 
                    AVG(cognitive_enhancement_score) as avg_passive_buff,
                    MAX(cognitive_enhancement_score) as max_passive_buff,
                    COUNT(*) as total_conversations,
                    AVG(learning_efficiency) as avg_learning_efficiency
                FROM knowledge.conversation_insights
                WHERE conversation_date >= CURRENT_DATE - INTERVAL ? DAYS
            """
            
            passive_buff_result = await self._execute_query(passive_buff_query, [days])
            
            return {
                "success": True,
                "analysis_period_days": days,
                "learning_velocity": velocity_result["rows"] if velocity_result["success"] else [],
                "pattern_recognition_trends": pattern_result["rows"] if pattern_result["success"] else [],
                "cognitive_function_effectiveness": cognitive_result["rows"][0] if cognitive_result["success"] and cognitive_result["rows"] else {},
                "passive_buff_statistics": passive_buff_result["rows"][0] if passive_buff_result["success"] and passive_buff_result["rows"] else {},
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Learning pattern analysis failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def generate_knowledge_assets(self, topic_filter: str = None, min_enhancement_score: float = 0.7) -> Dict[str, Any]:
        """Generate reusable knowledge assets from high-value insights"""
        try:
            # Find high-value insights for asset generation
            asset_query = """
                SELECT 
                    insight_id,
                    conversation_topic,
                    insight_content,
                    key_concepts,
                    cognitive_enhancement_score
                FROM knowledge.conversation_insights
                WHERE cognitive_enhancement_score >= ?
            """
            
            params = [min_enhancement_score]
            if topic_filter:
                asset_query += " AND conversation_topic ILIKE ?"
                params.append(f"%{topic_filter}%")
            
            asset_query += " ORDER BY cognitive_enhancement_score DESC LIMIT 20"
            
            insights_result = await self._execute_query(asset_query, params)
            
            if not insights_result["success"] or not insights_result["rows"]:
                return {
                    "success": True,
                    "message": "No high-value insights found for asset generation",
                    "assets": []
                }
            
            # Group insights by topic and generate assets
            assets = []
            topic_groups = {}
            
            for insight in insights_result["rows"]:
                topic = insight["conversation_topic"]
                if topic not in topic_groups:
                    topic_groups[topic] = []
                topic_groups[topic].append(insight)
            
            # Generate knowledge assets for each topic group
            for topic, topic_insights in topic_groups.items():
                if len(topic_insights) >= 2:  # Only create assets for topics with multiple insights
                    asset_id = f"asset_{topic.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}"
                    
                    # Combine insights into coherent asset
                    asset_content = f"# Knowledge Asset: {topic}\n\n"
                    asset_content += "## Key Insights\n\n"
                    
                    all_concepts = []
                    source_insights = []
                    
                    for insight in topic_insights:
                        asset_content += f"- {insight['insight_content'][:200]}...\n"
                        all_concepts.extend(insight['key_concepts'])
                        source_insights.append(insight['insight_id'])
                    
                    # Add concept summary
                    unique_concepts = list(set(all_concepts))
                    asset_content += f"\n## Key Concepts\n{', '.join(unique_concepts[:10])}\n"
                    
                    # Calculate asset scores
                    reusability_score = min(1.0, len(unique_concepts) / 10.0)
                    enhancement_value = sum(insight['cognitive_enhancement_score'] for insight in topic_insights) / len(topic_insights)
                    cross_project_applicability = reusability_score * enhancement_value
                    
                    # Store asset in database
                    asset_insert_query = """
                        INSERT INTO knowledge.knowledge_assets (
                            asset_id, asset_name, asset_type, asset_content,
                            source_insights, reusability_score, enhancement_value,
                            cross_project_applicability, generated_date
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
                    
                    await self._execute_query(asset_insert_query, [
                        asset_id, f"{topic} Knowledge Asset", "insight_synthesis",
                        asset_content, source_insights, reusability_score,
                        enhancement_value, cross_project_applicability, date.today()
                    ])
                    
                    assets.append({
                        "asset_id": asset_id,
                        "asset_name": f"{topic} Knowledge Asset",
                        "source_insight_count": len(topic_insights),
                        "reusability_score": reusability_score,
                        "enhancement_value": enhancement_value,
                        "content_preview": asset_content[:300] + "..."
                    })
            
            return {
                "success": True,
                "assets_generated": len(assets),
                "assets": assets,
                "min_enhancement_score": min_enhancement_score,
                "topic_filter": topic_filter
            }
            
        except Exception as e:
            logger.error(f"Knowledge asset generation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _execute_query(self, query: str, params: List[Any] = None) -> Dict[str, Any]:
        """Execute database query with parameter binding"""
        try:
            if params:
                result = self.connection.execute(query, params).fetchall()
            else:
                result = self.connection.execute(query).fetchall()
            
            columns = [desc[0] for desc in self.connection.description] if self.connection.description else []
            
            # Format results
            rows = []
            for row in result:
                row_dict = {}
                for i, value in enumerate(row):
                    column_name = columns[i] if i < len(columns) else f"column_{i}"
                    # Handle various data types
                    if isinstance(value, (int, float, str, bool, type(None))):
                        row_dict[column_name] = value
                    elif isinstance(value, list):
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

class MCPServer:
    """MCP Protocol Handler for Personal Knowledge Intelligence Server"""
    
    def __init__(self, db_path: str = ":memory:"):
        self.knowledge_intelligence = PersonalKnowledgeIntelligence(db_path)
    
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
                        "name": "personal-knowledge-intelligence-server",
                        "version": "1.0.0"
                    }
                }
            
            elif method == "tools/list":
                return {
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
                                        "description": "The conversation topic/category (default: general)",
                                        "default": "general"
                                    }
                                },
                                "required": ["conversation_content"]
                            }
                        },
                        {
                            "name": "search_knowledge_base",
                            "description": "Intelligent search across captured insights with pattern matching and relevance scoring",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "query": {
                                        "type": "string",
                                        "description": "Search query to find relevant insights"
                                    },
                                    "limit": {
                                        "type": "integer",
                                        "description": "Maximum number of results to return (default: 10)",
                                        "default": 10
                                    }
                                },
                                "required": ["query"]
                            }
                        },
                        {
                            "name": "analyze_learning_patterns",
                            "description": "Generate comprehensive learning analytics and cognitive optimization insights",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "days": {
                                        "type": "integer",
                                        "description": "Number of days to analyze (default: 30)",
                                        "default": 30
                                    }
                                },
                                "required": []
                            }
                        },
                        {
                            "name": "generate_knowledge_assets",
                            "description": "Generate reusable knowledge assets from high-value insights for maximum passive buff enhancement",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "topic_filter": {
                                        "type": "string",
                                        "description": "Filter assets by topic (optional)"
                                    },
                                    "min_enhancement_score": {
                                        "type": "number",
                                        "description": "Minimum cognitive enhancement score for asset generation (default: 0.7)",
                                        "default": 0.7
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
                
                if tool_name == "capture_conversation_insights":
                    result = await self.knowledge_intelligence.capture_conversation_insights(
                        tool_args.get("conversation_content"),
                        tool_args.get("topic", "general")
                    )
                elif tool_name == "search_knowledge_base":
                    result = await self.knowledge_intelligence.search_knowledge_base(
                        tool_args.get("query"),
                        tool_args.get("limit", 10)
                    )
                elif tool_name == "analyze_learning_patterns":
                    result = await self.knowledge_intelligence.analyze_learning_patterns(
                        tool_args.get("days", 30)
                    )
                elif tool_name == "generate_knowledge_assets":
                    result = await self.knowledge_intelligence.generate_knowledge_assets(
                        tool_args.get("topic_filter"),
                        tool_args.get("min_enhancement_score", 0.7)
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
    parser = argparse.ArgumentParser(description="Personal Knowledge Intelligence MCP Server")
    parser.add_argument("--db-path", default=":memory:", help="Path to knowledge database file")
    args = parser.parse_args()
    
    logger.info(f"Starting Personal Knowledge Intelligence MCP Server - The Ultimate Passive Buff System")
    logger.info(f"Knowledge Database: {args.db_path}")
    
    server = MCPServer(args.db_path)
    
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
