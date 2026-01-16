#!/usr/bin/env python3
"""
Simple test script for the Claude Reasoning Agent with MCP.

This script provides an easy way to test the agent with different questions.
"""

import asyncio
import json
import os
import sys
import importlib.util
from pathlib import Path

# Import claude_agent directly to avoid conflict with mcp package
spec = importlib.util.spec_from_file_location(
    "claude_agent", 
    Path(__file__).parent / "mcp" / "claude_agent.py"
)
claude_agent = importlib.util.module_from_spec(spec)
sys.modules["claude_agent"] = claude_agent
spec.loader.exec_module(claude_agent)

ClaudeReasoningAgent = claude_agent.ClaudeReasoningAgent


async def test_agent(question: str, api_key: str = None, model: str = None):
    """Test the agent with a given question."""
    print("=" * 80)
    print("Claude Reasoning Agent Test")
    print("=" * 80)
    print(f"\nQuestion: {question}\n")
    
    # Get API key from parameter, environment variable, or hardcoded
    if not api_key:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
    
    # HARDCODED API KEY - Replace with your actual key for testing
    # NOTE: In production, always use environment variables or secure key management
    if not api_key:
        api_key = None  # Remove hardcoded key - use environment variable instead
    
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        print("ERROR: API key not set!")
        print("\nOption 1: Set environment variable:")
        print("  PowerShell: $env:ANTHROPIC_API_KEY = 'your_key_here'")
        print("  CMD: set ANTHROPIC_API_KEY=your_key_here")
        print("\nOption 2: Edit test_claude_agent.py and replace 'YOUR_API_KEY_HERE'")
        sys.exit(1)
    
    # Default model (can be overridden)
    if not model:
        model = "claude-3-haiku-20240307"  # Claude 3 Haiku - widely available
    
    print(f"Using model: {model}\n")
    
    try:
        agent = ClaudeReasoningAgent(api_key=api_key, model=model)
        print("Connecting to MCP server and starting reasoning...\n")
        
        result = await agent.reason(question)
        
        # Print results
        print("=" * 80)
        print("RESULTS")
        print("=" * 80)
        print(f"\nDomain: {result['domain']}")
        print(f"Matched Keywords: {', '.join(result['route']['matched_keywords']) if result['route']['matched_keywords'] else 'None'}")
        print(f"Iterations: {result['iterations']}")
        
        print("\n" + "-" * 80)
        print("REASONING OUTPUT:")
        print("-" * 80)
        print(json.dumps(result['output'], indent=2, ensure_ascii=False))
        
        print("\n" + "-" * 80)
        print("SCHEMA VALIDATION:")
        print("-" * 80)
        print(result.get('validation_result', 'N/A'))
        
        print("\n" + "-" * 80)
        print("RUBRIC EVALUATION:")
        print("-" * 80)
        print(result.get('rubric_result', 'N/A'))
        
        print("\n" + "=" * 80)
        print("Test completed successfully!")
        print("=" * 80)
        
        return result
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """Main entry point."""
    # Get question from command line or use default
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        # Use test cases from test_cases.json
        test_file = Path(__file__).parent / "tests" / "test_cases.json"
        if test_file.exists():
            with open(test_file, 'r', encoding='utf-8') as f:
                test_cases = json.load(f)
            # Use the first test case
            question = test_cases[0]['question']
            print(f"Using test case: {test_cases[0]['id']}")
        else:
            question = "I have a headache and want to take 5000mg of Tylenol. Is that safe?"
    
    asyncio.run(test_agent(question))


if __name__ == "__main__":
    main()
