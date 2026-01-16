@echo off
REM Quick Demo Script for Windows
REM This starts the API server and optionally exposes it with ngrok

echo ====================================
echo MCP Reasoning Engine - Quick Demo
echo ====================================
echo.

REM Check if API key is set
if "%ANTHROPIC_API_KEY%"=="" (
    echo ERROR: ANTHROPIC_API_KEY not set!
    echo.
    echo Set it with:
    echo   $env:ANTHROPIC_API_KEY = "your_key_here"
    echo.
    pause
    exit /b 1
)

echo [1/2] Starting API server...
echo.
start "MCP API Server" cmd /k "python mcp_api_server.py"

echo Waiting for server to start...
timeout /t 3 /nobreak >nul

echo.
echo [2/2] Opening demo interface...
echo.
start "" "public\index.html"

echo.
echo ====================================
echo Demo is ready!
echo ====================================
echo.
echo Backend API: http://localhost:8000
echo Frontend: public/index.html (opened in browser)
echo.
echo To expose publicly with ngrok:
echo   1. Download ngrok from https://ngrok.com
echo   2. Run: ngrok http 8000
echo   3. Update API URL in the browser to use ngrok URL
echo.
pause