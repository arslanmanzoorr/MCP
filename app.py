#!/usr/bin/env python3
"""
FastAPI entry point for deployment platforms.

This file imports the FastAPI app from mcp_api_server.py
to satisfy platform requirements (Render, Railway, etc.)
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import the FastAPI app from mcp_api_server
from mcp_api_server import app

# Export the app for the platform
# This allows platforms to find the FastAPI app at the standard location
__all__ = ['app']