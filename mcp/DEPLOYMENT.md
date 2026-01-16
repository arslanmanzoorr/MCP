# Claude Agent + MCP Deployment Guide

This guide explains how to set up and test the Claude Reasoning Agent with MCP tools.

## Prerequisites

1. **Python 3.8+** installed
2. **Anthropic API Key** - Get one from https://console.anthropic.com/
3. All dependencies installed (see Installation below)

## Installation

1. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   
   # Windows:
   .venv\Scripts\activate
   
   # Linux/Mac:
   source .venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your Anthropic API key**:
   ```bash
   # Windows:
   set ANTHROPIC_API_KEY=your_api_key_here
   
   # Linux/Mac:
   export ANTHROPIC_API_KEY=your_api_key_here
   ```

   Or create a `.env` file (you'll need `python-dotenv` package):
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

## Testing

### Quick Test

Run the test script with a custom question:
```bash
python test_claude_agent.py "Your question here"
```

Or use the default test case:
```bash
python test_claude_agent.py
```

### Test with Different Questions

```bash
# Health question
python test_claude_agent.py "I have a headache and want to take 5000mg of Tylenol. Is that safe?"

# Legal question
python test_claude_agent.py "Is a verbal promise between friends to help move furniture enforceable?"

# Science question
python test_claude_agent.py "Can increased temperature explain faster reaction rates?"
```

### Using the Agent Directly

You can also use the agent directly from Python:

```python
import asyncio
from mcp.claude_agent import ClaudeReasoningAgent

async def main():
    agent = ClaudeReasoningAgent()
    result = await agent.reason("Your question here")
    print(result)

asyncio.run(main())
```

Or use the command-line interface:

```bash
python -m mcp.claude_agent --question "Your question here"
```

## How It Works

1. **MCP Server** (`mcp/server.py`):
   - Exposes three tools:
     - `search_knowledge_base`: Search RAG documents
     - `validate_reasoning_schema`: Validate JSON output against schema
     - `evaluate_with_rubric`: Score output against domain rubrics

2. **Claude Agent** (`mcp/claude_agent.py`):
   - Connects to MCP server via stdio
   - Uses Claude's Messages API with tool use
   - Orchestrates the reasoning workflow:
     - Searches knowledge base
     - Generates structured reasoning
     - Validates schema
     - Evaluates with rubric

3. **Test Script** (`test_claude_agent.py`):
   - Simple wrapper for easy testing
   - Handles API key checking
   - Pretty-prints results

## Architecture

```
┌─────────────────┐
│  Test Script    │
│ test_claude_... │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│ Claude Agent    │◄────►│  MCP Server  │
│ claude_agent.py │      │  server.py   │
└────────┬────────┘      └──────┬───────┘
         │                      │
         ▼                      ▼
┌─────────────────┐      ┌──────────────┐
│ Anthropic API   │      │ RAG Tools    │
│   (Claude)      │      │ Validators   │
└─────────────────┘      └──────────────┘
```

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
- Make sure you've set the environment variable
- Check that it's set in your current shell session
- Verify the API key is valid

### "No tools available from MCP server"
- Make sure `mcp/server.py` exists and is executable
- Check that all dependencies are installed
- Try running `python mcp/server.py` directly to see if there are import errors

### "ModuleNotFoundError"
- Make sure you're running from the project root directory
- Check that all dependencies in `requirements.txt` are installed
- Verify your virtual environment is activated

### Connection Issues
- Ensure Python can find all required modules
- Check that `mcp/server.py` can be executed with `python -m mcp.server` or `python mcp/server.py`

## File Structure

```
reasoning_engine_mcp_demo/
├── mcp/
│   ├── server.py          # MCP server with tools
│   ├── claude_agent.py    # Claude agent with MCP integration
│   └── DEPLOYMENT.md      # This file
├── test_claude_agent.py   # Test script
├── rag_docs/              # Knowledge base documents
├── schemas/               # JSON schemas
├── domains/               # Domain configs and rubrics
└── requirements.txt       # Dependencies
```

## Next Steps

- Customize the reasoning prompts in `claude_agent.py`
- Add more RAG documents in `rag_docs/`
- Create domain-specific rubrics in `domains/*/rubric.json`
- Extend the MCP server with additional tools
