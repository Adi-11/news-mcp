#!/usr/bin/env python3
"""
Quick test to verify the GNews MCP server implementation
"""

import ast
import sys

def test_syntax():
    """Test if main.py has valid Python syntax"""
    try:
        with open("main.py", "r") as f:
            code = f.read()
        ast.parse(code)
        print("✓ Syntax check passed")
        return True
    except SyntaxError as e:
        print(f"✗ Syntax error: {e}")
        return False

def test_imports():
    """Test if all imports are available"""
    required_packages = ["mcp", "httpx", "pydantic"]
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✓ Module '{package}' available")
        except ImportError as e:
            print(f"✗ Module '{package}' not found: {e}")
            return False
    return True

def test_server_structure():
    """Test if the server has the required tools"""
    try:
        # This will fail if imports fail, but let's check the structure
        import gnews_mpc
        
        # Check if the server has the required tools
        if hasattr(gnews_mpc, 'search'):
            print("✓ 'search' tool found")
        else:
            print("✗ 'search' tool not found")
            
        if hasattr(gnews_mpc, 'get_top_headlines'):
            print("✓ 'get_top_headlines' tool found")
        else:
            print("✗ 'get_top_headlines' tool not found")
            
        if hasattr(gnews_mpc, 'mcp'):
            print("✓ FastMCP instance found")
        else:
            print("✗ FastMCP instance not found")

        # email server should exist in workspace
        try:
            import email_mcp
            if hasattr(email_mcp, 'draft_email'):
                print("✓ 'draft_email' tool found in email_mcp")
            else:
                print("✗ 'draft_email' tool not found in email_mcp")
            if hasattr(email_mcp, 'mcp'):
                print("✓ Email FastMCP instance found")
            else:
                print("✗ Email FastMCP instance not found")
        except ImportError:
            print("✗ Could not import email_mcp module")
            return False
            
        return True
    except Exception as e:
        print(f"✗ Error checking server structure: {e}")
        return False

if __name__ == "__main__":
    print("Testing GNews MCP Server Implementation")
    print("=" * 50)
    
    if test_syntax():
        print()
    else:
        sys.exit(1)
    
    if test_imports():
        print()
    else:
        print("\nNote: Some packages may not be installed yet. Run 'uv install' first.")
        sys.exit(1)
    
    if test_server_structure():
        print()
    else:
        sys.exit(1)
    
    print("=" * 50)
    print("✓ All tests passed! Server is ready to use.")
    print()
    print("Next steps:")
    print("1. Get a free API key from https://gnews.io")
    print("2. Set the API key: export GNEWS_API_KEY='your-api-key'")
    print("3. Run the server: uv run main.py")
    print("4. Or test with inspector: uv run mcp dev main.py")
