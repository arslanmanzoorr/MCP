#!/usr/bin/env python3
"""
Test the MCP server directly with an LLM client.
This script starts the MCP server and tests all tools.
"""

import asyncio
import json
import sys
from pathlib import Path

from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

SERVER_SCRIPT = Path(__file__).parent / "mcp" / "server.py"


async def test_mcp_tools():
    """Test MCP tools directly."""
    print("=" * 80)
    print("Testing MCP Server Tools")
    print("=" * 80)
    print()
    
    # Set up MCP server connection
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_SCRIPT)],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            await session.initialize()
            
            # List available tools
            print("1. Listing available tools...")
            tools_result = await session.list_tools()
            print(f"   Found {len(tools_result.tools)} tools:")
            for tool in tools_result.tools:
                print(f"   - {tool.name}: {tool.description[:60]}...")
            print()
            
            # Test 1: Search knowledge base
            print("2. Testing search_knowledge_base...")
            search_result = await session.call_tool(
                "search_knowledge_base",
                arguments={"query": "contract enforceability"}
            )
            print(f"   Result preview: {search_result.content[0].text[:200]}...")
            print()
            
            # Test 2: Validate schema
            print("3. Testing validate_reasoning_schema...")
            test_json = json.dumps({
                "question": "Test question",
                "given_information": ["Test info"],
                "assumptions": ["Test assumption"],
                "reasoning_steps": ["Step 1", "Step 2"],
                "alternative_views": ["Alternative"],
                "limitations": ["Limitation"],
                "conclusion": "Test conclusion",
                "confidence": 0.8
            })
            schema_result = await session.call_tool(
                "validate_reasoning_schema",
                arguments={"output_json": test_json}
            )
            print(f"   Result: {schema_result.content[0].text}")
            print()
            
            # Test 3: Evaluate with rubric
            print("4. Testing evaluate_with_rubric...")
            rubric_result = await session.call_tool(
                "evaluate_with_rubric",
                arguments={
                    "domain": "legal",
                    "output_json": test_json
                }
            )
            print(f"   Result preview: {rubric_result.content[0].text[:300]}...")
            print()
            
            print("=" * 80)
            print("All MCP tools tested successfully!")
            print("=" * 80)


async def test_with_claude():
    """Test MCP tools with Claude using them."""
    import os
    
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("ERROR: API key not set!")
        print("\nSet environment variable:")
        print("  PowerShell: $env:ANTHROPIC_API_KEY = 'your_key_here'")
        print("  CMD: set ANTHROPIC_API_KEY=your_key_here")
        print("  Linux/Mac: export ANTHROPIC_API_KEY='your_key_here'")
        print("\nGet your API key from: https://console.anthropic.com/")
        return
    
    print("=" * 80)
    print("Testing MCP Server with Claude")
    print("=" * 80)
    print()
    
    client = Anthropic(api_key=api_key)
    
    # Set up MCP server connection
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_SCRIPT)],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            await session.initialize()
            
            # Get tools and convert to Anthropic format
            tools_result = await session.list_tools()
            anthropic_tools = []
            for tool in tools_result.tools:
                properties = {}
                required = []
                if hasattr(tool, 'inputSchema') and tool.inputSchema:
                    schema = tool.inputSchema
                    if "properties" in schema:
                        properties = schema["properties"]
                    if "required" in schema:
                        required = schema["required"]
                
                anthropic_tools.append({
                    "name": tool.name,
                    "description": tool.description or "No description",
                    "input_schema": {
                        "type": "object",
                        "properties": properties,
                        "required": required,
                    }
                })
            
            print(f"Connected to MCP server with {len(anthropic_tools)} tools")
            print()
            
            # Ask Claude to use the tools
            question = "What information do you have about contract enforceability?"
            
            print(f"Question: {question}")
            print()
            print("Claude is reasoning and using MCP tools...")
            print()
            
            messages = [{
                "role": "user",
                "content": f"{question}\n\nPlease use the search_knowledge_base tool to find relevant information, then provide a summary."
            }]
            
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=2048,
                messages=messages,
                tools=anthropic_tools,
            )
            
            print("Claude's Response:")
            print("-" * 80)
            
            # Process response and handle tool use
            tool_results = []
            for content_block in response.content:
                if content_block.type == "text":
                    print(content_block.text)
                elif content_block.type == "tool_use":
                    print(f"\n[Claude wants to use tool: {content_block.name}]")
                    print(f"  Input: {json.dumps(content_block.input, indent=2)}")
                    
                    # Call the tool
                    tool_result = await session.call_tool(
                        content_block.name,
                        arguments=content_block.input
                    )
                    result_text = tool_result.content[0].text
                    print(f"  Tool Result: {result_text[:300]}...")
                    
                    # Store for follow-up message
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": content_block.id,
                        "content": result_text
                    })
            
            # If Claude used tools, get the follow-up response
            if tool_results:
                print("\n" + "-" * 80)
                print("Getting Claude's response after tool use...")
                print("-" * 80)
                
                # Add tool results to messages
                messages.append({
                    "role": "assistant",
                    "content": response.content
                })
                messages.append({
                    "role": "user",
                    "content": tool_results
                })
                
                # Get Claude's response after seeing tool results
                follow_up = client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=2048,
                    messages=messages,
                    tools=anthropic_tools,
                )
                
                print("\nClaude's Final Response:")
                print("-" * 80)
                for block in follow_up.content:
                    if block.type == "text":
                        print(block.text)
                    elif block.type == "tool_use":
                        print(f"\n[Additional Tool Use: {block.name}]")
            
            print()
            print("=" * 80)
            print("Test completed!")
            print("=" * 80)


async def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test MCP server")
    parser.add_argument(
        "--with-claude",
        action="store_true",
        help="Test with Claude using the tools"
    )
    args = parser.parse_args()
    
    if args.with_claude:
        await test_with_claude()
    else:
        await test_mcp_tools()


if __name__ == "__main__":
    asyncio.run(main())
