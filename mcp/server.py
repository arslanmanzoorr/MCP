from datetime import datetime
import json
from pathlib import Path
from typing import Any, Dict, List

from mcp.server.fastmcp import FastMCP

# Import existing logic
# Adjust imports assuming this script is run from the repo root or we set PYTHONPATH.
# For simplicity, we'll assume we can import from the root if we append it to sys.path
import sys
import os

# Add parent directory to sys.path to allow imports from root
sys.path.append(str(Path(__file__).parent.parent))

from tools_rag import rag_search, RagChunk
from validators.schema_validator import validate_schema
from validators.rubric_validator import score_against_rubric

# Create the MCP server
mcp = FastMCP("Reasoning Engine")

# Define paths
BASE_DIR = Path(__file__).parent.parent
RAG_DOCS_DIR = BASE_DIR / "rag_docs"
SCHEMAS_DIR = BASE_DIR / "schemas"
DOMAINS_DIR = BASE_DIR / "domains"

@mcp.tool()
def search_knowledge_base(query: str) -> str:
    """
    Search the knowledge base (RAG docs) for relevant information.
    Returns a formatted string of the top results.
    """
    results = rag_search([str(RAG_DOCS_DIR)], query, k=3)
    
    if not results:
        return "No relevant documents found."
    
    formatted = []
    for chunk in results:
        formatted.append(f"Source: {Path(chunk.doc_id).name}\nTitle: {chunk.title}\nContent:\n{chunk.text}\n")
    
    return "\n---\n".join(formatted)

@mcp.tool()
def validate_reasoning_schema(output_json: str) -> str:
    """
    Validate that the reasoning output conforms to the required JSON schema.
    Pass the output as a JSON string.
    Returns "OK" if valid, or a list of error messages.
    """
    try:
        data = json.loads(output_json)
    except json.JSONDecodeError as e:
        return f"Invalid JSON: {e}"

    schema_path = SCHEMAS_DIR / "universal_reasoning_schema.json"
    valid, errors = validate_schema(data, schema_path)
    
    if valid:
        return "Schema Validation Passed: OK"
    else:
        return "Schema Validation Failed:\n" + "\n".join(errors)

@mcp.tool()
def evaluate_with_rubric(domain: str, output_json: str) -> str:
    """
    Evaluate the reasoning output against a domain-specific rubric.
    Supported domains: 'health', 'legal', 'science'.
    Pass the output as a JSON string.
    """
    try:
        data = json.loads(output_json)
    except json.JSONDecodeError as e:
        return f"Invalid JSON: {e}"
        
    rubric_path = DOMAINS_DIR / domain / "rubric.json"
    if not rubric_path.exists():
        return f"Error: Domain '{domain}' not found or no rubric available."

    result = score_against_rubric(domain, data, rubric_path)
    
    # Format the result nicely
    res_str = f"Rubric Score: {result.total}/{result.max_total} (Passed: {result.passed})\n"
    res_str += f"Needs Human Review: {result.needs_human_review}\n"
    res_str += "Breakdown:\n"
    for k, v in result.scores.items():
        res_str += f"- {k}: {v}\n"
    
    if result.flags:
        res_str += "\nFlags:\n"
        for f in result.flags:
            res_str += f"- {f}\n"
            
    return res_str

if __name__ == "__main__":
    mcp.run()
