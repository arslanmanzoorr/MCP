# 🎯 Client Demo Guide - MCP Reasoning Engine

A comprehensive guide for presenting and demonstrating the MCP Reasoning Engine to clients.

---

## 📋 Pre-Demo Checklist

### Before the Meeting

- [ ] **Test Everything First**
  ```bash
  # Run all tests to ensure everything works
  python run_all_tests.py
  ```

- [ ] **Set Up Environment**
  - API key configured: `$env:ANTHROPIC_API_KEY = "your_key_here"` (PowerShell)
  - Dependencies installed: `pip install -r requirements.txt`
  - Test that the API server starts: `python mcp_api_server.py`

- [ ] **Prepare Demo Questions**
  - Legal: "Is a verbal promise between friends to help move furniture enforceable?"
  - Health: "What could explain occasional chest discomfort and dizziness?"
  - Science: "Can increased temperature explain faster reaction rates?"

- [ ] **Know Your Architecture**
  - Understand the flow: HTTP API → Claude Agent → MCP Server → Tools
  - Be ready to explain the three domains (Legal, Health, Science)
  - Understand the three MCP tools (search, validate, evaluate)

- [ ] **Prepare Your Environment**
  - Close unnecessary applications
  - Have browser ready for API docs (http://localhost:8000/docs)
  - Have terminal/command prompt ready
  - Backup plan if internet is slow

---

## 🎬 Demo Script (15-20 minutes)

### Part 1: Introduction (2 minutes)

**Opening Statement:**
> "Today I'm going to show you our MCP Reasoning Engine - a production-ready AI system that combines Claude AI with structured knowledge tools to provide reliable reasoning across legal, health, and science domains."

**Key Points to Mention:**
- Built on Anthropic's Claude AI
- Uses Model Context Protocol (MCP) for tool integration
- Three specialized domains with domain-specific knowledge bases
- Automated validation and evaluation

---

### Part 2: Architecture Overview (3 minutes)

**Show the README.md or draw a diagram:**

```
HTTP API (Optional)
      ↓
Claude Agent
      ↓
MCP Server (3 Tools)
      ↓
┌─────┴─────┐
│           │
RAG Docs  Validators
(KB Search) (Schema + Rubric)
```

**Explain:**
1. **MCP Server** - Exposes three specialized tools
2. **RAG Integration** - Knowledge base search across domain documents
3. **Schema Validation** - Ensures structured JSON output
4. **Rubric Evaluation** - Domain-specific scoring and quality checks

---

### Part 3: Live Demo - API Server (5 minutes)

**Step 1: Start the Server**
```bash
python mcp_api_server.py
```

**Step 2: Show Interactive API Docs**
- Open browser: `http://localhost:8000/docs`
- Explain the Swagger UI interface
- Show the `/health` endpoint
- Show the `/tools` endpoint to list available tools

**Step 3: Run a Demo Query**

Use the `/reason` endpoint in Swagger UI or via curl:

```bash
curl -X POST http://localhost:8000/reason \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Is a verbal promise between friends to help move furniture enforceable?",
    "model": "claude-3-haiku-20240307"
  }'
```

**What to Highlight:**
- ✅ Automatic domain detection (Legal)
- ✅ Structured JSON output
- ✅ Schema validation passed
- ✅ Rubric evaluation with scores
- ✅ Iterative refinement if needed

---

### Part 4: Domain Examples (5 minutes)

**Show All Three Domains:**

**1. Legal Domain:**
```json
{
  "question": "Is a verbal promise between friends to help move furniture enforceable?"
}
```
- Highlights: Contract basics, enforceability reasoning

**2. Health Domain:**
```json
{
  "question": "What could explain occasional chest discomfort and dizziness?"
}
```
- Highlights: Safety boundaries, red flags, human review flags

**3. Science Domain:**
```json
{
  "question": "Can increased temperature explain faster reaction rates?"
}
```
- Highlights: Hypothesis formation, evidence evaluation

**Point Out:**
- Each domain has its own knowledge base (RAG docs)
- Each domain has a custom rubric for evaluation
- Automatic routing based on keywords

---

### Part 5: Code Walkthrough (Optional - 3 minutes)

If client is technical, show:

**1. Simple Python Usage:**
```python
from mcp.claude_agent import ClaudeReasoningAgent
import asyncio

async def main():
    agent = ClaudeReasoningAgent()
    result = await agent.reason("Your question here")
    print(result)

asyncio.run(main())
```

**2. Project Structure:**
- Show `mcp/` directory (server and agent)
- Show `rag_docs/` (knowledge bases)
- Show `domains/` (rubrics)
- Show `validators/` (validation logic)

---

### Part 6: Testing & Quality (2 minutes)

**Run Test Suite:**
```bash
python run_all_tests.py
```

**Show:**
- All tests passing
- Test coverage across domains
- Validation and rubric tests

---

## 💡 Key Selling Points to Emphasize

### 1. **Production-Ready**
- ✅ Full error handling
- ✅ Schema validation
- ✅ Rubric-based quality control
- ✅ HTTP API for integration
- ✅ Complete documentation

### 2. **Domain Expertise**
- ✅ Legal: Contract law, enforceability
- ✅ Health: Medical safety boundaries, symptom limits
- ✅ Science: Hypothesis formation, evidence evaluation

### 3. **Quality Assurance**
- ✅ Automatic schema validation
- ✅ Rubric-based scoring
- ✅ Human review flags for sensitive topics
- ✅ Iterative refinement until quality thresholds met

### 4. **Flexible Integration**
- ✅ HTTP REST API
- ✅ Direct Python library usage
- ✅ Docker-ready for deployment
- ✅ Easy to extend to new domains

### 5. **Built on Best Practices**
- ✅ MCP (Model Context Protocol) standard
- ✅ Claude AI (state-of-the-art reasoning)
- ✅ RAG (Retrieval-Augmented Generation)
- ✅ Structured output validation

---

## ❓ Handling Common Questions

### Q: "How accurate is this?"
**A:** The system uses Claude AI, which is state-of-the-art for reasoning tasks. We add layers of validation (schema validation, rubric evaluation) to ensure quality. For sensitive domains like health, we flag outputs for human review.

### Q: "Can we add our own knowledge base?"
**A:** Yes! Simply add documents to the `rag_docs/` directory in the appropriate domain folder. The system will automatically search them.

### Q: "How do we deploy this?"
**A:** We have multiple deployment options:
- Local/on-premise: Just run the Python server
- Docker: Containerized deployment (see `DEPLOYMENT_GUIDE.md`)
- Cloud: AWS, Azure, GCP compatible
- See `mcp/DEPLOYMENT.md` for detailed guides

### Q: "What about API costs?"
**A:** The system uses Claude API, and you can choose models based on cost/speed:
- Haiku: Fast, cost-effective (default)
- Sonnet: Balanced
- Opus: Most capable, higher cost

### Q: "Can it handle our domain?"
**A:** Absolutely! The system is designed to be extensible. You can:
1. Add a new domain folder in `domains/`
2. Add knowledge documents in `rag_docs/`
3. Configure routing in `domain_config.json`
4. Create a custom rubric for evaluation

### Q: "Is it secure?"
**A:** Yes:
- ✅ API keys via environment variables (never hardcoded)
- ✅ Input validation on all endpoints
- ✅ HTTPS recommended for production
- ✅ Health domain always flags for human review

### Q: "What's the response time?"
**A:** Depends on:
- Model choice (Haiku is fastest)
- Query complexity
- Number of iterations needed
- Typically 2-10 seconds for most queries

---

## 📊 Demo Metrics to Show

If relevant, prepare to show:
- Response times from test runs
- Test success rates (should be 100% if all tests pass)
- Number of domains supported (3)
- Number of tools available (3)
- Knowledge base size (number of RAG documents)

---

## 🎁 Post-Demo Follow-Up

### Immediate Next Steps
1. **Share Documentation**
   - `README.md` - Main documentation
   - `DEPLOYMENT_GUIDE.md` - Deployment options
   - `START_HERE.md` - Quick start guide

2. **Provide Access**
   - Source code repository
   - API endpoint (if deployed)
   - Test credentials (if applicable)

3. **Schedule Technical Deep Dive** (if needed)
   - Architecture discussion
   - Customization options
   - Integration planning

### Deliverables to Prepare
- [ ] Project source code (zip or git repo)
- [ ] Documentation package
- [ ] Deployment instructions
- [ ] Test results summary
- [ ] API endpoint URL (if deploying)

---

## 🚨 Troubleshooting During Demo

### If API Server Won't Start
**Quick Fix:**
```bash
# Check if port is in use
netstat -ano | findstr :8000  # Windows
lsof -i :8000  # Mac/Linux

# Change port
$env:MCP_PORT = "8001"
python mcp_api_server.py
```

### If API Key Error
**Quick Fix:**
```bash
# Windows PowerShell
$env:ANTHROPIC_API_KEY = "your_key_here"

# Verify it's set
echo $env:ANTHROPIC_API_KEY
```

### If Tests Fail
**Quick Fix:**
- Run individual tests to isolate issue
- Check that all dependencies are installed
- Verify API key is valid

### If Slow Response
**Explain:**
- First query may be slower (cold start)
- Subsequent queries are faster
- Consider using Haiku model for faster responses

---

## 📝 Customization Ideas to Mention

### Easy Customizations
1. **Add More Domains** - Copy domain folder structure
2. **Add Knowledge Documents** - Drop markdown files in `rag_docs/`
3. **Adjust Rubrics** - Edit `domains/*/rubric.json`
4. **Change Models** - Pass model parameter in API

### Advanced Customizations
1. **Custom Tools** - Add new MCP tools in `mcp/server.py`
2. **Custom Validation** - Extend validators in `validators/`
3. **Custom Routing** - Modify `router.py` logic
4. **Custom Schemas** - Update `schemas/universal_reasoning_schema.json`

---

## ✅ Post-Demo Checklist

- [ ] Send follow-up email with:
  - Links to documentation
  - Summary of demo points
  - Next steps/timeline
- [ ] Answer any pending questions
- [ ] Provide access credentials if deploying
- [ ] Schedule follow-up meeting if needed
- [ ] Document any custom requirements discussed

---

## 🎯 Success Criteria

A successful demo should demonstrate:
1. ✅ System works out-of-the-box
2. ✅ Clear architecture and design
3. ✅ Quality validation and evaluation
4. ✅ Multiple domain support
5. ✅ Easy to integrate and deploy
6. ✅ Professional and production-ready

---

**Good luck with your demo! 🚀**

For questions during demo prep, refer to:
- `README.md` - Technical details
- `DEPLOYMENT_GUIDE.md` - Deployment options
- `mcp/DEPLOYMENT.md` - MCP-specific deployment