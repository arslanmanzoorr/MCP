# Detailed API Test with Error Details

$apiUrl = "https://mcp-iota-seven.vercel.app"

Write-Host "=== Detailed API Test ===" -ForegroundColor Cyan
Write-Host ""

# Test /reason with error details
Write-Host "Testing /reason endpoint..." -ForegroundColor Green
$body = @{
    question = "Is a verbal promise between friends to help move furniture enforceable?"
    model = "claude-3-haiku-20240307"
} | ConvertTo-Json

try {
    Write-Host "Request body: $body" -ForegroundColor Gray
    Write-Host "Sending request..." -ForegroundColor Yellow
    
    $response = Invoke-WebRequest -Uri "$apiUrl/reason" -Method Post -Body $body -ContentType "application/json" -UseBasicParsing
    
    Write-Host "Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "Response:" -ForegroundColor Cyan
    Write-Host $response.Content -ForegroundColor White
    
} catch {
    Write-Host "Error occurred!" -ForegroundColor Red
    Write-Host "Status Code: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
    Write-Host "Status Description: $($_.Exception.Response.StatusDescription)" -ForegroundColor Red
    
    # Try to read error response
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host ""
        Write-Host "Error Response Body:" -ForegroundColor Yellow
        Write-Host $responseBody -ForegroundColor White
    } else {
        Write-Host "Error Message: $($_.Exception.Message)" -ForegroundColor Red
    }
}