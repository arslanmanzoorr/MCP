# Test MCP Reasoning Engine API

$apiUrl = "https://mcp-iota-seven.vercel.app"

Write-Host "=== Testing MCP Reasoning Engine API ===" -ForegroundColor Cyan
Write-Host "API URL: $apiUrl" -ForegroundColor Yellow
Write-Host ""

# Test 1: Health Check
Write-Host "1. Testing /health endpoint..." -ForegroundColor Green
try {
    $health = Invoke-RestMethod -Uri "$apiUrl/health" -Method Get
    Write-Host "   Status: $($health.status)" -ForegroundColor White
    Write-Host "   MCP Server: $($health.mcp_server)" -ForegroundColor White
    Write-Host "   Tools Available: $($health.tools_available)" -ForegroundColor White
    Write-Host "   API Key Configured: $($health.api_key_configured)" -ForegroundColor White
    Write-Host "   ✅ Health check passed!" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Health check failed: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 2: Tools List
Write-Host "2. Testing /tools endpoint..." -ForegroundColor Green
try {
    $tools = Invoke-RestMethod -Uri "$apiUrl/tools" -Method Get
    Write-Host "   Tools found: $($tools.tools.Count)" -ForegroundColor White
    foreach ($tool in $tools.tools) {
        Write-Host "   - $($tool.name): $($tool.description)" -ForegroundColor Gray
    }
    Write-Host "   ✅ Tools endpoint works!" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Tools endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 3: Reason Endpoint (Legal Question)
Write-Host "3. Testing /reason endpoint (Legal question)..." -ForegroundColor Green
$body = @{
    question = "Is a verbal promise between friends to help move furniture enforceable?"
    model = "claude-3-haiku-20240307"
} | ConvertTo-Json

try {
    Write-Host "   Sending request... (this may take 10-30 seconds)" -ForegroundColor Yellow
    $reason = Invoke-RestMethod -Uri "$apiUrl/reason" -Method Post -Body $body -ContentType "application/json"
    
    Write-Host "   Domain: $($reason.domain)" -ForegroundColor White
    Write-Host "   Iterations: $($reason.iterations)" -ForegroundColor White
    Write-Host "   ✅ Reason endpoint works!" -ForegroundColor Green
    Write-Host ""
    Write-Host "   Output preview:" -ForegroundColor Cyan
    Write-Host "   $($reason.output | ConvertTo-Json -Depth 2 -Compress)" -ForegroundColor Gray
} catch {
    Write-Host "   ❌ Reason endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   Error details: $($_.Exception.Response)" -ForegroundColor Red
}
Write-Host ""

Write-Host "=== Testing Complete ===" -ForegroundColor Cyan