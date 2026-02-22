#!/bin/bash
# Quick Start Guide for GNews MCP Server

# 1. Get an API key
echo "Step 1: Get a free GNews API key"
echo "---"
echo "1. Visit https://gnews.io"
echo "2. Create a free account"
echo "3. Copy your API key"
echo ""

# 2. Set API key
echo "Step 2: Set the API key"
echo "---"
echo "Run this command to set your API key:"
echo "  export GNEWS_API_KEY='your-api-key-here'"
echo ""

# 3. Run the server
echo "Step 3: Run the server"
echo "---"
echo "Option A: Run directly"
echo "  uv run main.py"
echo ""
echo "Option B: Test with MCP Inspector"
echo "  uv run mcp dev main.py"
echo "  Then open http://localhost:5000 in your browser"
echo ""
echo "Option C: Install in Claude Desktop"
echo "  uv run mcp install main.py --name 'GNews'"
echo ""

# 4. Available tools
echo "Step 4: Use the tools"
echo "---"
echo "The server provides two tools:"
echo ""
echo "1. search - Search for news articles"
echo "   Parameters:"
echo "   - q (required): Search keywords"
echo "   - lang (optional): Language code (e.g., 'en', 'fr', 'de')"
echo "   - country (optional): Country code (e.g., 'us', 'gb')"
echo "   - max_articles (optional): 1-100 (default: 10)"
echo "   - sort_by (optional): 'publishedAt' or 'relevance'"
echo ""
echo "   Example: search for 'Apple iPhone' in English"
echo ""
echo "2. get_top_headlines - Get trending articles by category"
echo "   Parameters:"
echo "   - category (optional): general, business, technology, sports, etc."
echo "   - lang (optional): Language code"
echo "   - country (optional): Country code"
echo "   - max_articles (optional): 1-100 (default: 10)"
echo ""
echo "   Example: get top technology headlines in the US"
echo ""

echo "For more details, see README.md"
