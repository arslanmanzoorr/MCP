"""
Claude Agent SDK integration with MCP tools.

This module provides a reasoning agent that uses Claude's Messages API
with tool use capabilities, where tools are provided via MCP.
"""

import asyncio
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from router import DomainRouter

# Path to the MCP server script
SERVER_SCRIPT = Path(__file__).parent / "server.py"

# System prompt for the reasoning agent
REASONING_SYSTEM_PROMPT = """You are a reasoning agent that helps answer questions by:
1. Searching relevant knowledge bases using the search_knowledge_base tool
2. Generating structured reasoning output following the universal reasoning schema
3. Validating your output using the validate_reasoning_schema tool
4. Evaluating your output using the evaluate_with_rubric tool

You must produce JSON output that matches this EXACT schema:
{
  "question": "string",
  "given_information": ["string"],
  "assumptions": ["string"],
  "reasoning_steps": ["string"],
  "alternative_views": ["string"],
  "limitations": ["string"],
  "conclusion": "string",
  "confidence": 0.0-1.0
}

IMPORTANT: After gathering information with tools, you MUST output your reasoning as a JSON object wrapped in triple backticks with "json" label, like this:
```json
{
  "question": "...",
  "given_information": [...],
  "assumptions": [...],
  "reasoning_steps": [...],
  "alternative_views": [...],
  "limitations": [...],
  "conclusion": "...",
  "confidence": 0.9
}
```

Then call validate_reasoning_schema with the JSON string to validate it.

For health-related questions, use domain="health" in evaluate_with_rubric.
For legal questions, use domain="legal".
For science questions, use domain="science".
"""


def extract_json_from_text(text: str) -> Optional[Dict[str, Any]]:
    """Extract JSON object from text, trying multiple strategies."""
    if not text:
        return None
    
    # Strategy 1: Look for JSON code blocks
    json_block_pattern = r'```json\s*(\{.*?\})\s*```'
    match = re.search(json_block_pattern, text, re.DOTALL)
    if match:
        try:
            parsed = json.loads(match.group(1))
            if isinstance(parsed, dict) and "question" in parsed and "conclusion" in parsed:
                return parsed
        except json.JSONDecodeError:
            pass
    
    # Strategy 2: Look for any JSON object with balanced braces
    # Find the first { and then find the matching }
    start_idx = text.find('{')
    if start_idx >= 0:
        brace_count = 0
        for i in range(start_idx, len(text)):
            if text[i] == '{':
                brace_count += 1
            elif text[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    json_str = text[start_idx:i+1]
                    try:
                        parsed = json.loads(json_str)
                        if isinstance(parsed, dict) and "question" in parsed and "conclusion" in parsed:
                            return parsed
                    except json.JSONDecodeError:
                        pass
                    break
    
    # Strategy 3: Try to find JSON after common markers
    markers = ['```', '```json', 'json:', 'JSON:', '{']
    for marker in markers:
        idx = text.find(marker)
        if idx >= 0:
            # Try to extract from this position
            for i in range(idx, len(text)):
                if text[i] == '{':
                    brace_count = 0
                    for j in range(i, min(i + 5000, len(text))):
                        if text[j] == '{':
                            brace_count += 1
                        elif text[j] == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                try:
                                    parsed = json.loads(text[i:j+1])
                                    if isinstance(parsed, dict) and "question" in parsed and "conclusion" in parsed:
                                        return parsed
                                except json.JSONDecodeError:
                                    pass
                                break
                    break
    
    return None


def mcp_tool_to_anthropic_tool(mcp_tool) -> Dict[str, Any]:
    """Convert an MCP tool definition to Anthropic tool format."""
    # Extract parameter schema
    properties = {}
    required = []
    
    if hasattr(mcp_tool, 'inputSchema') and mcp_tool.inputSchema:
        schema = mcp_tool.inputSchema
        if "properties" in schema:
            properties = schema["properties"]
        if "required" in schema:
            required = schema["required"]
    
    return {
        "name": mcp_tool.name,
        "description": mcp_tool.description or "No description available",
        "input_schema": {
            "type": "object",
            "properties": properties,
            "required": required,
        }
    }


class ClaudeReasoningAgent:
    """A reasoning agent powered by Claude that uses MCP tools."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-sonnet-20240229"):
        """
        Initialize the Claude reasoning agent.
        
        Args:
            api_key: Anthropic API key. If None, uses ANTHROPIC_API_KEY env var.
            model: Claude model to use.
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Anthropic API key required. Set ANTHROPIC_API_KEY environment variable "
                "or pass api_key parameter."
            )
        self.client = Anthropic(api_key=self.api_key)
        self.model = model
        self.router = DomainRouter(Path(__file__).parent.parent / "domains" / "domain_config.json")
        
    async def _get_mcp_tools(self, session: ClientSession) -> List[Dict[str, Any]]:
        """Get tools from MCP server and convert to Anthropic format."""
        tools_result = await session.list_tools()
        anthropic_tools = [mcp_tool_to_anthropic_tool(tool) for tool in tools_result.tools]
        return anthropic_tools
    
    async def _call_mcp_tool(self, session: ClientSession, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Call an MCP tool and return the result as a string."""
        result = await session.call_tool(tool_name, arguments=arguments)
        # Extract text from result content
        if result.content and len(result.content) > 0:
            return result.content[0].text
        return "No result returned from tool."
    
    async def reason(self, question: str, max_iterations: int = 10) -> Dict[str, Any]:
        """
        Perform reasoning on a question using Claude and MCP tools.
        
        Args:
            question: The question to reason about
            max_iterations: Maximum number of tool-use iterations
            
        Returns:
            Dict containing the reasoning result and metadata
        """
        # Route to determine domain
        route = self.router.route(question)
        domain = route.domain
        
        # Set up MCP server connection
        server_params = StdioServerParameters(
            command=sys.executable,
            args=[str(SERVER_SCRIPT)],
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize MCP session
                await session.initialize()
                
                # Get tools from MCP server
                anthropic_tools = await self._get_mcp_tools(session)
                
                if not anthropic_tools:
                    raise RuntimeError("No tools available from MCP server")
                
                # Prepare messages
                messages = [
                    {
                        "role": "user",
                        "content": f"Please help me reason about this question: {question}\n\n"
                                 f"Start by searching for relevant information, then generate a structured reasoning output.",
                    }
                ]
                
                # Conversation loop
                iteration = 0
                final_reasoning_output = None
                
                while iteration < max_iterations:
                    iteration += 1
                    
                    # Call Claude with current messages and tools
                    response = self.client.messages.create(
                        model=self.model,
                        max_tokens=4096,
                        system=REASONING_SYSTEM_PROMPT,
                        messages=messages,
                        tools=anthropic_tools,
                    )
                    
                    # Add assistant message
                    assistant_message_content = []
                    messages.append({
                        "role": "assistant",
                        "content": response.content,
                    })
                    
                    # Debug: Try to extract JSON from text blocks immediately
                    for content_block in response.content:
                        if content_block.type == "text":
                            text = content_block.text
                            parsed = extract_json_from_text(text)
                            if parsed:
                                final_reasoning_output = parsed
                                break  # Exit early if we found JSON
                    
                    # Process tool use requests
                    tool_use_count = 0
                    for content_block in response.content:
                        if content_block.type == "tool_use":
                            tool_use_count += 1
                            tool_name = content_block.name
                            tool_input = content_block.input
                            
                            # Call the MCP tool
                            tool_result = await self._call_mcp_tool(session, tool_name, tool_input)
                            
                            # Add tool result to messages
                            messages.append({
                                "role": "user",
                                "content": [
                                    {
                                        "type": "tool_result",
                                        "tool_use_id": content_block.id,
                                        "content": tool_result,
                                    }
                                ],
                            })
                            
                            # If this is a schema validation that passed, extract the JSON
                            if tool_name == "validate_reasoning_schema" and "OK" in tool_result:
                                # Try to find the reasoning output in the conversation
                                # Look for JSON in previous messages
                                for msg in reversed(messages):
                                    if msg["role"] == "assistant":
                                        for block in msg.get("content", []):
                                            if isinstance(block, dict) and block.get("type") == "text":
                                                text = block.get("text", "")
                                                parsed = extract_json_from_text(text)
                                                if parsed:
                                                    final_reasoning_output = parsed
                                                    break
                    
                    # If no tool use, check if we got final answer
                    if tool_use_count == 0:
                        # Check if response contains final reasoning output
                        for content_block in response.content:
                            if content_block.type == "text":
                                text = content_block.text
                                parsed = extract_json_from_text(text)
                                if parsed:
                                    final_reasoning_output = parsed
                                    break
                        
                        # If we have final output, we're done
                        if final_reasoning_output:
                            break
                    
                    # Safety check - if too many iterations, extract what we have
                    if iteration >= max_iterations:
                        # Try one more time to get structured output
                        final_prompt = (
                            f"Extract or generate the final reasoning output as JSON matching the schema. "
                            f"Question: {question}\n\n"
                            f"Return ONLY valid JSON, no other text."
                        )
                        final_response = self.client.messages.create(
                            model=self.model,
                            max_tokens=2048,
                            messages=[{"role": "user", "content": final_prompt}],
                        )
                        
                        for block in final_response.content:
                            if block.type == "text":
                                parsed = extract_json_from_text(block.text)
                                if parsed:
                                    final_reasoning_output = parsed
                                    break
                        break
                
                # Validate final output
                validation_result = None
                rubric_result = None
                
                if final_reasoning_output:
                    # Validate schema
                    validation_json = json.dumps(final_reasoning_output)
                    validation_result = await self._call_mcp_tool(
                        session, 
                        "validate_reasoning_schema", 
                        {"output_json": validation_json}
                    )
                    
                    # Evaluate with rubric
                    rubric_result = await self._call_mcp_tool(
                        session,
                        "evaluate_with_rubric",
                        {"domain": domain, "output_json": validation_json}
                    )
                else:
                    # If we couldn't extract structured output, create a fallback
                    final_reasoning_output = {
                        "question": question,
                        "given_information": [],
                        "assumptions": ["Could not extract structured reasoning output"],
                        "reasoning_steps": ["Reasoning process completed but output extraction failed"],
                        "alternative_views": [],
                        "limitations": ["Failed to generate properly structured output"],
                        "conclusion": "Unable to provide a structured conclusion due to output extraction issues.",
                        "confidence": 0.1,
                    }
                
                return {
                    "domain": domain,
                    "route": {
                        "domain": route.domain,
                        "matched_keywords": route.matched_keywords,
                    },
                    "output": final_reasoning_output,
                    "validation_result": validation_result,
                    "rubric_result": rubric_result,
                    "iterations": iteration,
                }


async def main():
    """Test the Claude reasoning agent."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run Claude reasoning agent with MCP tools")
    parser.add_argument(
        "--question",
        type=str,
        default="I have a headache and want to take 5000mg of Tylenol. Is that safe?",
        help="Question to reason about",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="claude-3-sonnet-20240229",
        help="Claude model to use",
    )
    args = parser.parse_args()
    
    print("=" * 80)
    print("Claude Reasoning Agent with MCP Tools")
    print("=" * 80)
    print(f"Question: {args.question}")
    print()
    
    try:
        agent = ClaudeReasoningAgent(model=args.model)
        result = await agent.reason(args.question)
        
        print(f"Domain: {result['domain']}")
        print(f"Matched Keywords: {result['route']['matched_keywords']}")
        print(f"Iterations: {result['iterations']}")
        print()
        
        print("Reasoning Output:")
        print(json.dumps(result['output'], indent=2, ensure_ascii=False))
        print()
        
        if result['validation_result']:
            print("Schema Validation:")
            print(result['validation_result'])
            print()
        
        if result['rubric_result']:
            print("Rubric Evaluation:")
            print(result['rubric_result'])
            print()
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
