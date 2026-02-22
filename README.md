# GNews MCP Server

A Model Context Protocol (MCP) server that integrates the [GNews API](https://gnews.io) for searching and retrieving news articles.

## Features

- **search**: Search for news articles using keywords with support for:
  - Logical operators (AND, OR, NOT)
  - Phrase searches with quotes
  - Multiple languages and countries
  - Date range filtering
  - Sorting by relevance or publication date
  - Pagination

- **get_top_headlines**: Get trending news articles by category with support for:
  - 9 news categories (general, business, technology, sports, etc.)
  - Multiple languages and countries
  - Optional keyword filtering
  - Date range filtering
  - Pagination

## Installation

### Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- A free [GNews API key](https://gnews.io) (get one for free at https://gnews.io)

### Setup

1. Clone or navigate to the project directory:
```bash
cd gnews-mcp
```

2. Install dependencies:
```bash
uv install
```

Or with pip:
```bash
pip install -e .
```

## Configuration

### Getting an API Key

1. Visit [gnews.io](https://gnews.io)
2. Sign up for a free account
3. Copy your API key from the dashboard

### Setting the API Key

Set your GNews API key as an environment variable:

```bash
# Linux/macOS
export GNEWS_API_KEY='your-api-key-here'

# Windows (PowerShell)
$env:GNEWS_API_KEY='your-api-key-here'

# Or create a .env file and load it
echo "GNEWS_API_KEY=your-api-key-here" > .env
```

## Running the Server

### Direct Execution

```bash
# With API key set in environment
GNEWS_API_KEY='your-api-key' uv run main.py
```

### Development Mode with MCP Inspector

Test and debug the server using the MCP Inspector:

```bash
# Terminal 1: Start the server
GNEWS_API_KEY='your-api-key' uv run mcp dev main.py

# Terminal 2: In another terminal, start the inspector
npx -y @modelcontextprotocol/inspector

# Open http://localhost:5000 in your browser
```

### Install in Claude Desktop

```bash
uv run mcp install main.py --name "GNews"
```

Then configure in your Claude Desktop config file:

**macOS/Linux**: `~/.config/claude/claude_desktop_config.json`
```json
{
  "mcpServers": {
    "gnews": {
      "command": "uv",
      "args": ["--directory", "/path/to/gnews-mcp", "run", "main.py"],
      "env": {
        "GNEWS_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
```json
{
  "mcpServers": {
    "gnews": {
      "command": "uv",
      "args": ["--directory", "C:\\path\\to\\gnews-mcp", "run", "main.py"],
      "env": {
        "GNEWS_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

## Tool Reference

### search

Search for news articles using keywords.

**Parameters:**
- `q` (required): Search keywords
  - Supports logical operators: `AND`, `OR`, `NOT`
  - Supports phrase searches: `"exact phrase"`
  - Examples: `"Apple iPhone"`, `Apple OR Microsoft`, `Tesla AND NOT Model S`
- `lang` (optional): Language code (default: `en`)
  - Examples: `en`, `fr`, `de`, `es`, `ja`, etc.
- `country` (optional): Country code
  - Examples: `us`, `gb`, `fr`, `de`, `jp`, etc.
- `max_articles` (optional): Number of results (1-100, default: 10)
- `page` (optional): Page number for pagination (default: 1)
- `sort_by` (optional): Sort order (default: `publishedAt`)
  - Options: `publishedAt`, `relevance`
- `from_date` (optional): Filter from date (ISO 8601 format)
  - Example: `2025-02-01T00:00:00Z`
- `to_date` (optional): Filter until date (ISO 8601 format)

**Example:**
```
Search for "Apple iPhone 16" in English, sorted by relevance, maximum 5 articles
```

### get_top_headlines

Get trending news articles by category.

**Parameters:**
- `category` (optional): News category (default: `general`)
  - Options: `general`, `world`, `nation`, `business`, `technology`, `entertainment`, `sports`, `science`, `health`
- `lang` (optional): Language code (default: `en`)
- `country` (optional): Country code
- `max_articles` (optional): Number of results (1-100, default: 10)
- `page` (optional): Page number for pagination (default: 1)
- `query` (optional): Additional keyword filter
- `from_date` (optional): Filter from date (ISO 8601 format)
- `to_date` (optional): Filter until date (ISO 8601 format)

**Example:**
```
Get top 10 technology headlines in the US
```

## Example Queries

### Search Examples

1. Find articles about AI breakthroughs:
   ```
   search(q="artificial intelligence breakthrough", lang="en", max_articles=10)
   ```

2. Search for Tesla news excluding Model S:
   ```
   search(q="Tesla AND NOT Model S", lang="en", max_articles=15)
   ```

3. Find news from a specific date range:
   ```
   search(
     q="climate change",
     lang="en",
     country="us",
     from_date="2025-01-01T00:00:00Z",
     to_date="2025-02-21T23:59:59Z",
     max_articles=20
   )
   ```

4. Search for exact phrase in news titles:
   ```
   search(q='"renewable energy"', lang="en", max_articles=10)
   ```

### Top Headlines Examples

1. Get trending tech news in US:
   ```
   get_top_headlines(category="technology", country="us", lang="en", max_articles=10)
   ```

2. Get health news in multiple languages:
   ```
   get_top_headlines(category="health", lang="fr", country="fr", max_articles=5)
   ```

3. Get business headlines with optional filtering:
   ```
   get_top_headlines(
     category="business",
     country="gb",
     lang="en",
     query="fintech",
     max_articles=15
   )
   ```

## Response Format

Both tools return a structured response with:

```python
{
  "totalArticles": 42,  # Total articles found matching criteria
  "articles": [
    {
      "title": "Article Title",
      "description": "Article summary...",
      "url": "https://example.com/article",
      "image": "https://example.com/image.jpg",
      "source": "Source Name",
      "publishedAt": "2025-02-20T10:30:00Z"
    },
    ...
  ]
}
```

## Supported Languages

Arabic, Bengali, Chinese, Dutch, English, French, German, Greek, Hebrew, Hindi, Indonesian, Italian, Japanese, Malayalam, Marathi, Norwegian, Portuguese, Punjabi, Romanian, Russian, Spanish, Swedish, Tamil, Telugu, Turkish, Ukrainian, and more.

## Supported Countries

Argentina, Australia, Austria, Bangladesh, Brazil, Canada, China, France, Germany, India, Japan, Mexico, Netherlands, Russia, Spain, UK, US, and many more.

See [GNews documentation](https://docs.gnews.io) for complete lists.

## API Limits

- Free tier articles: Limited by subscription
- Maximum results per request: 100 articles
- Maximum pagination: 1000 articles (10 pages of 100)
- Rate limits: Depend on subscription level

## Troubleshooting

### API Key Error
- Ensure `GNEWS_API_KEY` environment variable is set correctly
- Get a free key at https://gnews.io

### Rate Limit Error
- You've exceeded the free tier limits
- Upgrade your plan at https://gnews.io/pricing

### No Results
- Try simpler search keywords
- Check your language and country codes
- Verify the date range parameters are correct

### Timeout Issues
- Try with fewer articles (`max_articles=5`)
- Check your internet connection
- The API may be temporarily unavailable

## Development

### Project Structure

```
gnews-mcp/
├── main.py              # Main MCP server implementation
├── pyproject.toml       # Project dependencies and metadata
└── README.md           # This file
```

### Testing

Test tools directly using the MCP Inspector:

```bash
GNEWS_API_KEY='your-key' uv run mcp dev main.py
```

### Contributing

Feel free to extend this server with additional features:
- Caching of results
- More advanced filtering
- Integration with other news APIs
- Custom category definitions

## License

MIT

## Resources

- [GNews API Documentation](https://docs.gnews.io)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [Python SDK Documentation](https://github.com/modelcontextprotocol/python-sdk)
