# Deployment Guide: MCP Reasoning Engine

This guide covers different ways to deploy and use your MCP server with Claude Agent.

## Quick Start (Local Development)

### 1. Prerequisites

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key
# Windows PowerShell:
$env:ANTHROPIC_API_KEY = "your_key_here"

# Linux/Mac:
export ANTHROPIC_API_KEY="your_key_here"
```

### 2. Test Locally

```bash
# Test MCP server tools
python test_mcp_server.py

# Test with Claude
python test_mcp_server.py --with-claude

# Test full agent
python test_claude_agent.py "Your question here"

# Run all tests
python run_all_tests.py
```

## Deployment Options

### Option 1: Local Deployment (Current Setup)

**Use Case**: Development, testing, or single-user scenarios

**How it works**: MCP server runs as a subprocess via stdio

**Status**: ✅ Already working! Your current setup is ready.

**To use**:
```bash
python test_claude_agent.py "Your question"
```

### Option 2: Server-Side Deployment (Python Service)

**Use Case**: Multi-user, API service, or cloud deployment

#### Step 1: Create an HTTP Wrapper

Create `mcp_api_server.py`:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import sys
from pathlib import Path

# Your existing agent code
sys.path.insert(0, str(Path(__file__).parent))
from mcp.claude_agent import ClaudeReasoningAgent

app = FastAPI(title="MCP Reasoning API")

class QuestionRequest(BaseModel):
    question: str
    model: str = "claude-3-haiku-20240307"

class ReasoningResponse(BaseModel):
    domain: str
    output: dict
    validation_result: str
    rubric_result: str
    iterations: int

@app.post("/reason", response_model=ReasoningResponse)
async def reason(request: QuestionRequest):
    """Process a reasoning question using MCP tools and Claude."""
    try:
        agent = ClaudeReasoningAgent(model=request.model)
        result = await agent.reason(request.question)
        return ReasoningResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "MCP Reasoning Engine"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

#### Step 2: Install Additional Dependencies

```bash
pip install fastapi uvicorn pydantic
```

#### Step 3: Run the Server

```bash
python mcp_api_server.py
```

#### Step 4: Test the API

```bash
# Using curl
curl -X POST http://localhost:8000/reason \
  -H "Content-Type: application/json" \
  -d '{"question": "Is a verbal promise enforceable?"}'

# Using Python
import requests
response = requests.post(
    "http://localhost:8000/reason",
    json={"question": "Is a verbal promise enforceable?"}
)
print(response.json())
```

### Option 3: Docker Deployment

**Use Case**: Containerized deployment, cloud platforms

#### Step 1: Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install FastAPI for HTTP deployment (optional)
RUN pip install fastapi uvicorn pydantic

# Copy application code
COPY . .

# Set environment variable (or use secrets management)
# ENV ANTHROPIC_API_KEY=your_key_here

# Expose port (if using HTTP API)
EXPOSE 8000

# Run the API server
CMD ["python", "mcp_api_server.py"]
```

#### Step 2: Build and Run

```bash
# Build
docker build -t mcp-reasoning-engine .

# Run
docker run -p 8000:8000 \
  -e ANTHROPIC_API_KEY=your_key_here \
  mcp-reasoning-engine

# Or use docker-compose
```

#### Step 3: Docker Compose (Optional)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  mcp-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - ./rag_docs:/app/rag_docs
      - ./domains:/app/domains
      - ./schemas:/app/schemas
```

Run:
```bash
docker-compose up
```

### Option 4: Cloud Deployment

#### AWS Lambda / Azure Functions / Google Cloud Functions

Wrap the agent in a serverless function handler. The MCP server subprocess approach works well here.

#### AWS EC2 / Azure VM / GCP Compute

1. Deploy using Docker (Option 3)
2. Use a reverse proxy (nginx) for HTTPS
3. Set up environment variables via secrets manager

#### Example: AWS Lambda Handler

```python
import json
import asyncio
from mcp.claude_agent import ClaudeReasoningAgent

def lambda_handler(event, context):
    question = event.get('question', '')
    
    # Run async agent
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    agent = ClaudeReasoningAgent()
    result = loop.run_until_complete(agent.reason(question))
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
```

## Environment Variables

### Required
- `ANTHROPIC_API_KEY`: Your Anthropic API key

### Optional
- `MCP_MODEL`: Claude model to use (default: claude-3-haiku-20240307)
- `MCP_PORT`: HTTP API port (default: 8000)

## Production Checklist

- [ ] Set `ANTHROPIC_API_KEY` via secure secrets management
- [ ] Enable HTTPS (use nginx, Caddy, or cloud load balancer)
- [ ] Set up logging and monitoring
- [ ] Configure rate limiting
- [ ] Set up health checks (`/health` endpoint)
- [ ] Backup RAG documents and domain configurations
- [ ] Test all three domains (legal, health, science)
- [ ] Monitor API costs and usage

## Monitoring and Logging

### Add Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

### Health Check Endpoint

```python
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "mcp_server": "operational",
        "tools_available": 3
    }
```

## Troubleshooting Deployment

### MCP Server Not Starting
- Check Python path and dependencies
- Verify `mcp/server.py` is executable
- Check file permissions

### API Key Issues
- Verify environment variable is set
- Check secrets manager configuration
- Ensure API key has proper permissions

### Port Conflicts
- Change port in `mcp_api_server.py`
- Check firewall rules
- Verify no other service on the port

## Security Considerations

1. **API Keys**: Never commit keys to git. Use environment variables or secrets managers
2. **HTTPS**: Always use HTTPS in production
3. **Rate Limiting**: Implement rate limiting to prevent abuse
4. **Input Validation**: Validate all user inputs
5. **Error Handling**: Don't expose sensitive errors to clients

## Next Steps

1. Choose your deployment option
2. Set up environment variables
3. Test deployment locally
4. Deploy to staging
5. Monitor and iterate

For specific deployment platforms, see:
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [AWS Lambda Python](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html)
