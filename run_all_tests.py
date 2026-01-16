#!/usr/bin/env python3
"""
Run all test cases from test_cases.json
"""

import asyncio
import json
import sys
import importlib.util
from pathlib import Path

# Import claude_agent
spec = importlib.util.spec_from_file_location(
    "claude_agent", 
    Path(__file__).parent / "mcp" / "claude_agent.py"
)
claude_agent = importlib.util.module_from_spec(spec)
sys.modules["claude_agent"] = claude_agent
spec.loader.exec_module(claude_agent)

ClaudeReasoningAgent = claude_agent.ClaudeReasoningAgent


async def run_test_case(agent, test_case, test_num, total):
    """Run a single test case."""
    print("\n" + "=" * 80)
    print(f"TEST {test_num}/{total}: {test_case['id']}")
    print("=" * 80)
    print(f"Domain Hint: {test_case.get('domain_hint', 'N/A')}")
    print(f"Question: {test_case['question']}")
    print()
    
    try:
        result = await agent.reason(test_case['question'])
        
        print(f"[OK] Domain: {result['domain']}")
        print(f"[OK] Iterations: {result['iterations']}")
        print(f"[OK] Schema Valid: {'OK' if 'OK' in str(result.get('validation_result', '')) else 'FAILED'}")
        
        rubric_result = result.get('rubric_result', '')
        if 'Passed: True' in str(rubric_result):
            print(f"[OK] Rubric: PASSED")
        elif 'Passed: False' in str(rubric_result):
            print(f"[FAIL] Rubric: FAILED")
        else:
            print(f"[?] Rubric: Unknown")
        
        if result.get('output', {}).get('confidence'):
            print(f"[OK] Confidence: {result['output']['confidence']}")
        
        print(f"[OK] Conclusion: {result.get('output', {}).get('conclusion', 'N/A')[:100]}...")
        
        return True, result
        
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return False, None


async def main():
    """Run all test cases."""
    import os
    
    # Get API key from environment
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("ERROR: API key not set!")
        print("\nSet environment variable:")
        print("  PowerShell: $env:ANTHROPIC_API_KEY = 'your_key_here'")
        print("  CMD: set ANTHROPIC_API_KEY=your_key_here")
        print("  Linux/Mac: export ANTHROPIC_API_KEY='your_key_here'")
        print("\nGet your API key from: https://console.anthropic.com/")
        sys.exit(1)
    
    model = "claude-3-haiku-20240307"
    
    print("=" * 80)
    print("RUNNING ALL TEST CASES")
    print("=" * 80)
    print(f"Model: {model}")
    print(f"API Key: {'*' * 20}...{api_key[-10:]}")
    print()
    
    # Load test cases
    test_file = Path(__file__).parent / "tests" / "test_cases.json"
    if not test_file.exists():
        print(f"ERROR: Test file not found: {test_file}")
        sys.exit(1)
    
    with open(test_file, 'r', encoding='utf-8') as f:
        test_cases = json.load(f)
    
    print(f"Found {len(test_cases)} test case(s)")
    print()
    
    # Initialize agent
    agent = ClaudeReasoningAgent(api_key=api_key, model=model)
    
    # Run all tests
    results = []
    for i, test_case in enumerate(test_cases, 1):
        success, result = await run_test_case(agent, test_case, i, len(test_cases))
        results.append({
            'id': test_case['id'],
            'success': success,
            'result': result
        })
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for r in results if r['success'])
    failed = len(results) - passed
    
    print(f"Total Tests: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print()
    
    for r in results:
        status = "[PASS]" if r['success'] else "[FAIL]"
        print(f"{status}: {r['id']}")
        if r['success'] and r['result']:
            output = r['result'].get('output', {})
            confidence = output.get('confidence', 0)
            rubric_passed = 'Passed: True' in str(r['result'].get('rubric_result', ''))
            print(f"     Confidence: {confidence}, Rubric: {'PASS' if rubric_passed else 'FAIL'}")
    
    print("=" * 80)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
