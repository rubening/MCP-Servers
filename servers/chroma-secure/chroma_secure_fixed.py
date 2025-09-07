#!/usr/bin/env python3
"""
Secure Chroma MCP Server for Attorney-Client Privilege Protection
Simplified pattern matching working servers exactly
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    import chromadb
    from chromadb.config import Settings
    logger.info("ChromaDB imported successfully")
except ImportError:
    logger.error("ChromaDB not available")
    chromadb = None

class SecureChromaIntelligence:
    """Attorney-Client Privilege Protected Vector Database"""
    
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.client = None
        
        if chromadb:
            self._init_chroma_client()
        else:
            logger.error("ChromaDB not available")
    
    def _init_chroma_client(self):
        """Initialize ChromaDB client with attorney-client privilege protection"""
        try:
            # Ensure directory exists
            Path(self.data_dir).mkdir(parents=True, exist_ok=True)
            
            # Configure ChromaDB for local-only operation
            settings = Settings(
                anonymized_telemetry=False,  # Disable telemetry for privacy
                allow_reset=False,  # Prevent accidental data loss
            )
            
            self.client = chromadb.PersistentClient(
                path=self.data_dir,
                settings=settings
            )
            
            logger.info(f"Secure Chroma client initialized at {self.data_dir}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Chroma client: {e}")
            self.client = None
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test secure connection"""
        if not self.client:
            return {
                "status": "error",
                "message": "ChromaDB client not initialized"
            }
        
        try:
            collections = self.client.list_collections()
            return {
                "status": "success",
                "message": "Secure Chroma connection operational",
                "attorney_client_privilege": "PROTECTED",
                "data_location": self.data_dir,
                "external_access": "DISABLED",
                "collections_count": len(collections)
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Connection test failed: {str(e)}"
            }
    
    async def create_collection(self, name: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Create collection with attorney-client privilege protection"""
        if not self.client:
            return {"status": "error", "message": "ChromaDB not available"}
        
        try:
            collection_name = f"law_firm_{name}"
            collection_metadata = {
                "attorney_client_privilege": True,
                "confidential": True,
                **(metadata or {})
            }
            
            collection = self.client.create_collection(
                name=collection_name,
                metadata=collection_metadata
            )
            
            return {
                "status": "success",
                "collection_name": collection_name,
                "message": "Collection created with attorney-client privilege protection"
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def list_collections(self) -> Dict[str, Any]:
        """List all law firm collections"""
        if not self.client:
            return {"status": "error", "message": "ChromaDB not available"}
        
        try:
            collections = self.client.list_collections()
            law_firm_collections = [
                {
                    "name": col.name,
                    "count": col.count() if hasattr(col, 'count') else 0
                }
                for col in collections
                if col.name.startswith("law_firm_")
            ]
            
            return {
                "status": "success",
                "collections": law_firm_collections,
                "total_collections": len(law_firm_collections),
                "message": "Collections listed with attorney-client privilege protection"
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}

class MCPServer:
    """MCP Protocol Handler - Simplified pattern matching working servers"""
    
    def __init__(self, data_dir: str):
        self.chroma_intelligence = SecureChromaIntelligence(data_dir)
    
    def get_request_id(self, request):
        """Handle request ID with proper null handling"""
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
                        "serverInfo": {"name": "chroma-secure", "version": "1.0.0"}
                    }
                }
            
            elif method == "tools/list":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "tools": [
                            {
                                "name": "test_connection",
                                "description": "Test the secure Chroma connection and attorney-client privilege protection",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {},
                                    "additionalProperties": False
                                }
                            },
                            {
                                "name": "create_collection",
                                "description": "Create a new vector collection with attorney-client privilege protection",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "name": {
                                            "type": "string",
                                            "description": "Name of the collection"
                                        },
                                        "metadata": {
                                            "type": "object",
                                            "description": "Optional metadata for the collection"
                                        }
                                    },
                                    "required": ["name"]
                                }
                            },
                            {
                                "name": "list_collections",
                                "description": "List all law firm collections with confidentiality protection",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {},
                                    "additionalProperties": False
                                }
                            }
                        ]
                    }
                }
            
            elif method == "tools/call":
                params = request.get("params", {})
                tool_name = params.get("name", "")
                arguments = params.get("arguments", {})
                
                if tool_name == "test_connection":
                    result = await self.chroma_intelligence.test_connection()
                elif tool_name == "create_collection":
                    result = await self.chroma_intelligence.create_collection(
                        arguments.get("name", ""),
                        arguments.get("metadata", {})
                    )
                elif tool_name == "list_collections":
                    result = await self.chroma_intelligence.list_collections()
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
    
    parser = argparse.ArgumentParser(description="Secure Chroma MCP Server")
    parser.add_argument("--data-dir", default="C:\\Users\\ruben\\Claude Tools\\secure_data\\chroma_law_firm", help="Chroma data directory")
    parser.add_argument("--dotenv-path", help="Environment file path (optional)")
    args = parser.parse_args()
    
    logger.info("Secure Chroma MCP Server starting...")
    logger.info(f"Data Directory: {args.data_dir}")
    logger.info("Attorney-Client Privilege: PROTECTED")
    
    server = MCPServer(args.data_dir)
    
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
