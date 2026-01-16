# Setup Instructions

## Initial Setup

1. **Extract/Clone the project**
   ```bash
   cd reasoning_engine_mcp_demo
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   
   # Activate
   # Windows:
   .venv\Scripts\activate
   
   # Linux/Mac:
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API key**
   ```bash
   # Windows PowerShell:
   $env:ANTHROPIC_API_KEY = "your_key_here"
   
   # Windows CMD:
   set ANTHROPIC_API_KEY=your_key_here
   
   # Linux/Mac:
   export ANTHROPIC_API_KEY="your_key_here"
   ```

5. **Verify installation**
   ```bash
   python -c "from mcp.claude_agent import ClaudeReasoningAgent; print('Setup successful!')"
   ```

## Quick Test

```bash
# Test MCP server
python test_mcp_server.py

# Test with a question
python -m mcp.claude_agent --question "Is a verbal promise enforceable?"
```

## Next Steps

- See `README.md` for usage examples
- See `mcp/DEPLOYMENT.md` for deployment options
- Visit `http://localhost:8000/docs` when running API server
