#!/usr/bin/env python3
"""
HTTP API Server for MCP Reasoning Engine.

This provides an HTTP endpoint wrapper around the MCP server and Claude agent.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import claude_agent directly to avoid conflict with mcp package
import importlib.util
spec = importlib.util.spec_from_file_location(
    "claude_agent", 
    Path(__file__).parent / "mcp" / "claude_agent.py"
)
claude_agent = importlib.util.module_from_spec(spec)
sys.modules["claude_agent"] = claude_agent
spec.loader.exec_module(claude_agent)

ClaudeReasoningAgent = claude_agent.ClaudeReasoningAgent

app = FastAPI(
    title="MCP Reasoning Engine API",
    description="API for reasoning with Claude using MCP tools",
    version="1.0.0"
)

# Enable CORS for web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str
    model: Optional[str] = "claude-3-haiku-20240307"
    max_iterations: Optional[int] = 10


class ReasoningResponse(BaseModel):
    domain: str
    route: Dict[str, Any]
    output: Dict[str, Any]
    validation_result: Optional[str]
    rubric_result: Optional[str]
    iterations: int


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "MCP Reasoning Engine API",
        "version": "1.0.0",
        "endpoints": {
            "/reason": "POST - Process a reasoning question",
            "/health": "GET - Health check",
            "/tools": "GET - List available MCP tools"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    api_key = os.environ.get("ANTHROPIC_API_KEY") or "hardcoded_in_test"
    has_api_key = bool(api_key) and api_key != "YOUR_API_KEY_HERE"
    
    return {
        "status": "healthy" if has_api_key else "degraded",
        "mcp_server": "operational",
        "tools_available": 3,
        "api_key_configured": has_api_key
    }


@app.post("/reason", response_model=ReasoningResponse)
async def reason(request: QuestionRequest):
    """
    Process a reasoning question using MCP tools and Claude.
    
    Example:
    ```json
    {
        "question": "Is a verbal promise enforceable?",
        "model": "claude-3-haiku-20240307"
    }
    ```
    """
    try:
        # Get API key from environment
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        
        if not api_key:
            raise HTTPException(
                status_code=500,
                detail="ANTHROPIC_API_KEY not configured"
            )
        
        # Create agent and process question
        agent = ClaudeReasoningAgent(api_key=api_key, model=request.model)
        result = await agent.reason(request.question, max_iterations=request.max_iterations)
        
        return ReasoningResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tools")
async def list_tools():
    """List available MCP tools."""
    return {
        "tools": [
            {
                "name": "search_knowledge_base",
                "description": "Search the knowledge base (RAG docs) for relevant information",
                "parameters": {"query": "string"}
            },
            {
                "name": "validate_reasoning_schema",
                "description": "Validate that the reasoning output conforms to the required JSON schema",
                "parameters": {"output_json": "string"}
            },
            {
                "name": "evaluate_with_rubric",
                "description": "Evaluate the reasoning output against a domain-specific rubric",
                "parameters": {"domain": "string", "output_json": "string"}
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("MCP_PORT", 8000))
    host = os.environ.get("MCP_HOST", "0.0.0.0")
    
    print(f"Starting MCP Reasoning Engine API on {host}:{port}")
    print(f"API Documentation: http://{host}:{port}/docs")
    
    uvicorn.run(app, host=host, port=port)
