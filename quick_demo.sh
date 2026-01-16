#!/bin/bash
# Quick Demo Script for Mac/Linux
# This starts the API server and opens the demo interface

echo "===================================="
echo "MCP Reasoning Engine - Quick Demo"
echo "===================================="
echo ""

# Check if API key is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "ERROR: ANTHROPIC_API_KEY not set!"
    echo ""
    echo "Set it with:"
    echo "  export ANTHROPIC_API_KEY='your_key_here'"
    echo ""
    exit 1
fi

echo "[1/2] Starting API server..."
python3 mcp_api_server.py &
SERVER_PID=$!

echo "Waiting for server to start..."
sleep 3

echo ""
echo "[2/2] Opening demo interface..."
echo ""

# Try to open browser (works on Mac/Linux)
if command -v xdg-open > /dev/null; then
    xdg-open "public/index.html"
elif command -v open > /dev/null; then
    open "public/index.html"
else
    echo "Please open public/index.html in your browser"
fi

echo ""
echo "===================================="
echo "Demo is ready!"
echo "===================================="
echo ""
echo "Backend API: http://localhost:8000"
echo "Frontend: public/index.html"
echo ""
echo "To expose publicly with ngrok:"
echo "  1. Install ngrok: https://ngrok.com"
echo "  2. Run: ngrok http 8000"
echo "  3. Update API URL in browser to use ngrok URL"
echo ""
echo "Press Ctrl+C to stop the server"
wait $SERVER_PID