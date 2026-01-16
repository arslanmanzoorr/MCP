# 🚀 Quick Reference Card - Client Demo

## Pre-Demo (5 min setup)

```bash
# 1. Set API key
$env:ANTHROPIC_API_KEY = "your_key_here"  # PowerShell

# 2. Test it works
python run_all_tests.py

# 3. Start server
python mcp_api_server.py
```

**Browser:** http://localhost:8000/docs

---

## Demo Questions (Copy & Paste Ready)

### Legal Domain
```json
{
  "question": "Is a verbal promise between friends to help move furniture enforceable?"
}
```

### Health Domain
```json
{
  "question": "What could explain occasional chest discomfort and dizziness?"
}
```

### Science Domain
```json
{
  "question": "Can increased temperature explain faster reaction rates?"
}
```

---

## Key Talking Points (30 seconds each)

1. **What It Is:** Claude AI + MCP tools for structured reasoning across 3 domains
2. **Key Features:** RAG search, schema validation, rubric evaluation
3. **Domains:** Legal (contracts), Health (medical safety), Science (hypotheses)
4. **Quality:** Automatic validation + scoring + human review flags
5. **Integration:** HTTP API or direct Python library

---

## Architecture Flow

```
Question → API → Claude Agent → MCP Server → Tools → Response
                                           ↓
                    ┌──────────┬──────────┴──────────┬──────────┐
                    │          │                     │          │
                RAG Search  Schema Valid  Rubric Eval
```

---

## Key Endpoints

- `GET /health` - Health check
- `GET /tools` - List MCP tools (3 tools)
- `POST /reason` - Main reasoning endpoint

---

## If Something Goes Wrong

**Server won't start?**
- Check port: Change `$env:MCP_PORT = "8001"`
- Check API key: `echo $env:ANTHROPIC_API_KEY`

**Slow response?**
- Normal for first query (cold start)
- Using Haiku model (fastest option)

**Tests fail?**
- Check dependencies: `pip install -r requirements.txt`
- Verify API key is valid

---

## Post-Demo

- [ ] Send README.md and DEPLOYMENT_GUIDE.md
- [ ] Answer any questions
- [ ] Schedule follow-up if needed

---

**💡 Tip:** Have terminal and browser ready before demo starts!