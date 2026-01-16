# MCP Reasoning Engine with Claude Agent

A production-ready reasoning engine that combines Claude AI with Model Context Protocol (MCP) tools for structured reasoning across legal, health, and science domains.

## Features

- 🤖 **Claude Agent Integration**: Uses Anthropic's Claude API with tool use capabilities
- 🔧 **MCP Tools**: Three specialized tools for knowledge search, schema validation, and rubric evaluation
- 📚 **RAG Integration**: Knowledge base search across domain-specific documents
- ✅ **Schema Validation**: Ensures structured JSON output matches required schemas
- 📊 **Rubric Scoring**: Domain-specific evaluation with pass/fail thresholds
- 🌐 **HTTP API**: RESTful API for easy integration
- 🐳 **Docker Ready**: Containerized deployment support

## Architecture

```
┌─────────────────┐
│   HTTP API      │  (Optional - mcp_api_server.py)
│   or Direct     │
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
│ Anthropic API   │      │ RAG Tools   │
│   (Claude)      │      │ Validators   │
└─────────────────┘      └──────────────┘
```

## Quick Start

### Prerequisites

- Python 3.8+
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Installation

1. **Clone or extract the project**
   ```bash
   cd reasoning_engine_mcp_demo
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set API key**
   ```bash
   # Windows PowerShell
   $env:ANTHROPIC_API_KEY = "your_api_key_here"
   
   # Linux/Mac
   export ANTHROPIC_API_KEY="your_api_key_here"
   ```

### Usage

#### Option 1: Direct Python Usage

```python
import asyncio
from mcp.claude_agent import ClaudeReasoningAgent

async def main():
    agent = ClaudeReasoningAgent()
    result = await agent.reason("Is a verbal promise enforceable?")
    print(result)

asyncio.run(main())
```

#### Option 2: Command Line

```bash
python -m mcp.claude_agent --question "Your question here"
```

#### Option 3: HTTP API Server

```bash
# Start server
python mcp_api_server.py

# Server runs on http://localhost:8000
# API docs: http://localhost:8000/docs
```

**API Example:**
```bash
curl -X POST http://localhost:8000/reason \
  -H "Content-Type: application/json" \
  -d '{"question": "Is a verbal promise enforceable?"}'
```

## Project Structure

```
reasoning_engine_mcp_demo/
├── mcp/                          # MCP server and agent
│   ├── server.py                # MCP server with 3 tools
│   ├── claude_agent.py          # Claude agent with MCP integration
│   └── DEPLOYMENT.md            # Deployment guide
├── rag_docs/                    # Knowledge base documents
│   ├── legal/                   # Legal domain documents
│   ├── health/                  # Health domain documents
│   └── science/                 # Science domain documents
├── domains/                     # Domain configurations
│   ├── domain_config.json       # Domain routing config
│   ├── legal/rubric.json        # Legal rubric
│   ├── health/rubric.json       # Health rubric
│   └── science/rubric.json      # Science rubric
├── schemas/                     # JSON schemas
│   └── universal_reasoning_schema.json
├── validators/                  # Validation modules
│   ├── schema_validator.py
│   └── rubric_validator.py
├── tools_rag.py                 # RAG search implementation
├── router.py                    # Domain routing
├── mcp_api_server.py            # HTTP API server
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## MCP Tools

The MCP server exposes three tools:

1. **search_knowledge_base(query: str)**
   - Searches RAG documents for relevant information
   - Returns formatted results with source, title, and content

2. **validate_reasoning_schema(output_json: str)**
   - Validates JSON output against the universal reasoning schema
   - Returns validation status and errors

3. **evaluate_with_rubric(domain: str, output_json: str)**
   - Evaluates reasoning output against domain-specific rubric
   - Returns scores, pass/fail status, and human review flags

## Domains

The system supports three domains:

- **Legal**: Contract law, enforceability, legal reasoning
- **Health**: Medical information, symptoms, safety boundaries
- **Science**: Scientific reasoning, hypotheses, evidence evaluation

Each domain has:
- Domain-specific RAG documents
- Custom rubric for evaluation
- Keyword-based routing

## Configuration

### Environment Variables

- `ANTHROPIC_API_KEY` (required): Your Anthropic API key
- `MCP_PORT` (optional): HTTP API port (default: 8000)
- `MCP_HOST` (optional): HTTP API host (default: 0.0.0.0)

### Model Selection

Default model: `claude-3-haiku-20240307`

To use a different model:
```python
agent = ClaudeReasoningAgent(model="claude-3-sonnet-20240229")
```

Available models:
- `claude-3-haiku-20240307` (fast, cost-effective)
- `claude-3-sonnet-20240229` (balanced)
- `claude-3-opus-20240229` (most capable)

## API Documentation

When running the HTTP API server, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /tools` - List available MCP tools
- `POST /reason` - Process a reasoning question

## Testing

```bash
# Test MCP server tools
python test_mcp_server.py

# Test with Claude
python test_mcp_server.py --with-claude

# Run all test cases
python run_all_tests.py
```

## Deployment

See `mcp/DEPLOYMENT.md` for detailed deployment instructions including:
- Local deployment
- Docker containerization
- Cloud deployment (AWS, Azure, GCP)
- Production best practices

## Security Notes

- **API Keys**: Never commit API keys to version control
- **Health Domain**: Always requires human review (configured in rubric)
- **Input Validation**: All inputs are validated before processing
- **HTTPS**: Use HTTPS in production environments

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
- Ensure environment variable is set in your shell session
- Check that it's set before running Python scripts

### "ModuleNotFoundError: No module named 'mcp.claude_agent'"
- This is a namespace conflict with the `mcp` package
- The code handles this automatically via importlib
- If issues persist, check Python path configuration

### "Model not found" errors
- Verify your API key has access to the requested model
- Try using `claude-3-haiku-20240307` (most widely available)

## License

[Specify your license here]

## Support

For issues or questions, please refer to:
- `mcp/DEPLOYMENT.md` - Deployment guide
- `DEPLOYMENT_GUIDE.md` - Detailed deployment options
- API documentation at `/docs` endpoint

## Changelog

### Version 1.0.0
- Initial release
- MCP server with 3 tools
- Claude agent integration
- HTTP API server
- Domain routing and rubric evaluation
- Full test suite# MCP
# MCP
