#!/usr/bin/env python3
"""
Demo Readiness Checker

Run this script before your client demo to ensure everything is set up correctly.
"""

import os
import sys
import json
from pathlib import Path

def check_file_exists(path, description):
    """Check if a file or directory exists."""
    if Path(path).exists():
        print(f"✅ {description}: {path}")
        return True
    else:
        print(f"❌ {description}: {path} - MISSING!")
        return False

def check_python_packages():
    """Check if required Python packages are installed."""
    required_packages = [
        'anthropic',
        'fastapi',
        'uvicorn',
        'pydantic',
        'jsonschema',
        'requests',
        'mcp'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ Package installed: {package}")
        except ImportError:
            print(f"❌ Package missing: {package}")
            missing.append(package)
    
    return len(missing) == 0

def check_api_key():
    """Check if API key is set."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if api_key and api_key != "YOUR_API_KEY_HERE" and api_key.strip():
        print(f"✅ API key is set (length: {len(api_key)} chars)")
        return True
    else:
        print("❌ API key is NOT set!")
        print("   Set it with: $env:ANTHROPIC_API_KEY = 'your_key_here' (PowerShell)")
        return False

def check_test_cases():
    """Check if test cases file exists."""
    test_file = Path("tests/test_cases.json")
    if test_file.exists():
        try:
            with open(test_file, 'r') as f:
                test_cases = json.load(f)
            print(f"✅ Test cases file found ({len(test_cases)} test cases)")
            return True
        except:
            print("❌ Test cases file exists but is invalid JSON")
            return False
    else:
        print("❌ Test cases file missing: tests/test_cases.json")
        return False

def check_critical_files():
    """Check if all critical files exist."""
    files_to_check = [
        ("README.md", "Main documentation"),
        ("requirements.txt", "Dependencies file"),
        ("mcp_api_server.py", "API server"),
        ("mcp/server.py", "MCP server"),
        ("mcp/claude_agent.py", "Claude agent"),
        ("domains/domain_config.json", "Domain configuration"),
        ("schemas/universal_reasoning_schema.json", "Reasoning schema"),
        ("router.py", "Domain router"),
        ("tools_rag.py", "RAG tools"),
        ("validators/schema_validator.py", "Schema validator"),
        ("validators/rubric_validator.py", "Rubric validator"),
    ]
    
    all_present = True
    for path, desc in files_to_check:
        if not check_file_exists(path, desc):
            all_present = False
    
    return all_present

def check_rag_docs():
    """Check if RAG documents exist."""
    domains = ['legal', 'health', 'science']
    all_present = True
    
    for domain in domains:
        rag_dir = Path(f"rag_docs/{domain}")
        if rag_dir.exists():
            doc_count = len(list(rag_dir.glob("*.md")))
            print(f"✅ RAG docs for {domain}: {doc_count} documents")
        else:
            print(f"❌ RAG docs missing for {domain}: rag_docs/{domain}/")
            all_present = False
    
    return all_present

def check_rubrics():
    """Check if rubrics exist."""
    domains = ['legal', 'health', 'science']
    all_present = True
    
    for domain in domains:
        rubric_file = Path(f"domains/{domain}/rubric.json")
        if rubric_file.exists():
            print(f"✅ Rubric exists for {domain}")
        else:
            print(f"❌ Rubric missing for {domain}: domains/{domain}/rubric.json")
            all_present = False
    
    return all_present

def main():
    """Run all checks."""
    print("=" * 70)
    print("DEMO READINESS CHECK")
    print("=" * 70)
    print()
    
    checks = []
    
    print("📁 Checking critical files...")
    checks.append(("Critical Files", check_critical_files()))
    print()
    
    print("📚 Checking RAG documents...")
    checks.append(("RAG Documents", check_rag_docs()))
    print()
    
    print("📊 Checking rubrics...")
    checks.append(("Rubrics", check_rubrics()))
    print()
    
    print("🧪 Checking test cases...")
    checks.append(("Test Cases", check_test_cases()))
    print()
    
    print("📦 Checking Python packages...")
    checks.append(("Python Packages", check_python_packages()))
    print()
    
    print("🔑 Checking API key...")
    checks.append(("API Key", check_api_key()))
    print()
    
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    all_passed = True
    for check_name, passed in checks:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {check_name}")
        if not passed:
            all_passed = False
    
    print()
    
    if all_passed:
        print("🎉 ALL CHECKS PASSED! You're ready for the demo!")
        print()
        print("Next steps:")
        print("1. Start the server: python mcp_api_server.py")
        print("2. Open browser: http://localhost:8000/docs")
        print("3. Follow the demo guide: CLIENT_DEMO_GUIDE.md")
    else:
        print("⚠️  SOME CHECKS FAILED! Please fix the issues above before demo.")
        print()
        print("Common fixes:")
        print("- Install packages: pip install -r requirements.txt")
        print("- Set API key: $env:ANTHROPIC_API_KEY = 'your_key_here'")
        print("- Check that all files from delivery package are present")
    
    print("=" * 70)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())