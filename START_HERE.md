# 🚀 START HERE - MCP Reasoning Engine

Welcome! This is your complete MCP Reasoning Engine package.

## Quick Navigation

1. **First Time Setup?** → Read `SETUP.md`
2. **Want to Use It?** → Read `README.md`
3. **Need to Deploy?** → Read `mcp/DEPLOYMENT.md`
4. **What's Included?** → Read `DELIVERY_PACKAGE.md`

## 5-Minute Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your API key
export ANTHROPIC_API_KEY="your_key_here"  # Linux/Mac
# OR
$env:ANTHROPIC_API_KEY = "your_key_here"  # Windows PowerShell

# 3. Test it works
python run_all_tests.py

# 4. Start the API server
python mcp_api_server.py
```

Then visit: **http://localhost:8000/docs** for interactive API documentation!

## What You Get

✅ **MCP Server** - 3 specialized tools for reasoning  
✅ **Claude Agent** - AI-powered reasoning engine  
✅ **HTTP API** - RESTful API for integration  
✅ **3 Domains** - Legal, Health, Science  
✅ **Full Test Suite** - Verify everything works  
✅ **Complete Docs** - Setup, deployment, API reference  

## Key Files

- `README.md` - Main documentation and usage
- `mcp_api_server.py` - HTTP API server (start here for API)
- `mcp/claude_agent.py` - Core agent (use for direct Python)
- `mcp/server.py` - MCP server implementation

## Need Help?

- **Setup Issues?** → `SETUP.md`
- **Deployment?** → `mcp/DEPLOYMENT.md` or `DEPLOYMENT_GUIDE.md`
- **API Usage?** → Visit `/docs` when server is running
- **Testing?** → `python run_all_tests.py`

## Important Notes

⚠️ **API Key Required**: You must provide your own Anthropic API key  
⚠️ **Python 3.8+**: Required for this project  
⚠️ **Virtual Environment**: Recommended for isolation  

---

**Ready to start?** → Open `SETUP.md` and follow the instructions!
