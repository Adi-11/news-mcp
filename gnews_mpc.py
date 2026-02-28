"""
GNews MCP Server - Integrates GNews API for news search and top headlines
"""

import os
from typing import Optional

import httpx
from pydantic import BaseModel, Field

from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP(
    name="GNews Server",
    instructions="Search and retrieve news articles from GNews API. Use search for keywords and get_top_headlines for trending articles."
)

# Get API key from environment
GNEWS_API_KEY = os.environ.get("GNEWS_API_KEY", "0ab29b86c167605488334a0ece87e197")
GNEWS_BASE_URL = "https://gnews.io/api/v4"

# Timeout for HTTP requests
HTTP_TIMEOUT = 10.0


class Article(BaseModel):
    """News article model"""

    title: str = Field(description="Article title")
    description: Optional[str] = Field(default=None, description="Article description")
    url: str = Field(description="URL to the article")
    image: Optional[str] = Field(default=None, description="Image URL")
    source: str = Field(description="News source")
    publishedAt: str = Field(description="Publication date in ISO 8601 format")


class SearchResult(BaseModel):
    """Search results model"""

    totalArticles: int = Field(description="Total number of articles found")
    articles: list[Article] = Field(description="List of articles")


@mcp.tool()
async def search(
    q: str,
    lang: str = "en",
    country: Optional[str] = None,
    max_articles: int = 10,
    page: int = 1,
    sort_by: str = "publishedAt",
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
) -> SearchResult:
    """
    Search for news articles using keywords.

    Args:
        q: Search keywords (supports logical operators: AND, OR, NOT, and quotes for phrases)
        lang: Language code (e.g., 'en', 'fr', 'de'). Default: 'en'
        country: Country code (e.g., 'us', 'gb', 'fr'). Optional.
        max_articles: Number of articles to return (1-100). Default: 10
        page: Page number for pagination. Default: 1
        sort_by: Sort order - 'publishedAt' or 'relevance'. Default: 'publishedAt'
        from_date: Filter articles from this date (ISO 8601 format). Optional.
        to_date: Filter articles until this date (ISO 8601 format). Optional.

    Returns:
        SearchResult: Total count and list of articles matching the search criteria
    """
    if not GNEWS_API_KEY:
        raise ValueError(
            "GNEWS_API_KEY environment variable not set. Please set your GNews API key."
        )

    if not q:
        raise ValueError("Search query (q) is required and cannot be empty")

    # Validate max_articles
    max_articles = max(1, min(max_articles, 100))

    # Build query parameters
    params = {
        "q": q,
        "apikey": GNEWS_API_KEY,
        "lang": lang,
        "max": max_articles,
        "page": page,
        "sortby": sort_by,
    }

    # Add optional parameters
    if country:
        params["country"] = country
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date

    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            response = await client.get(f"{GNEWS_BASE_URL}/search", params=params)
            response.raise_for_status()

            data = response.json()

            # Check for API errors
            if data.get("errors"):
                errors_str = ", ".join(data["errors"])
                raise ValueError(f"GNews API errors: {errors_str}")

            # Parse articles
            articles = [
                Article(
                    title=article["title"],
                    description=article.get("description"),
                    url=article["url"],
                    image=article.get("image"),
                    source=article["source"]["name"],
                    publishedAt=article["publishedAt"],
                )
                for article in data.get("articles", [])
            ]

            return SearchResult(
                totalArticles=data.get("totalArticles", 0), articles=articles
            )

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise ValueError("Invalid API key. Please check your GNEWS_API_KEY.")
        elif e.response.status_code == 429:
            raise ValueError(
                "API rate limit exceeded. Please try again later."
            )
        else:
            raise ValueError(f"API request failed: {e.response.status_code}")
    except httpx.TimeoutException:
        raise ValueError("API request timed out. Please try again.")
    except Exception as e:
        raise ValueError(f"Failed to search articles: {str(e)}")


@mcp.tool()
async def get_top_headlines(
    category: str = "general",
    lang: str = "en",
    country: Optional[str] = None,
    max_articles: int = 10,
    page: int = 1,
    query: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
) -> SearchResult:
    """
    Get top trending news headlines by category.

    Args:
        category: News category. Options: general, world, nation, business,
                 technology, entertainment, sports, science, health. Default: 'general'
        lang: Language code (e.g., 'en', 'fr', 'de'). Default: 'en'
        country: Country code (e.g., 'us', 'gb', 'fr'). Optional.
        max_articles: Number of articles to return (1-100). Default: 10
        page: Page number for pagination. Default: 1
        query: Optional search keywords to filter results further. Optional.
        from_date: Filter articles from this date (ISO 8601 format). Optional.
        to_date: Filter articles until this date (ISO 8601 format). Optional.

    Returns:
        SearchResult: Total count and list of trending articles in the selected category
    """
    if not GNEWS_API_KEY:
        raise ValueError(
            "GNEWS_API_KEY environment variable not set. Please set your GNews API key."
        )

    # Validate category
    valid_categories = {
        "general",
        "world",
        "nation",
        "business",
        "technology",
        "entertainment",
        "sports",
        "science",
        "health",
    }
    if category not in valid_categories:
        raise ValueError(
            f"Invalid category '{category}'. Must be one of: {', '.join(sorted(valid_categories))}"
        )

    # Validate max_articles
    max_articles = max(1, min(max_articles, 100))

    # Build query parameters
    params = {
        "category": category,
        "apikey": GNEWS_API_KEY,
        "lang": lang,
        "max": max_articles,
        "page": page,
    }

    # Add optional parameters
    if country:
        params["country"] = country
    if query:
        params["q"] = query
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date

    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            response = await client.get(
                f"{GNEWS_BASE_URL}/top-headlines", params=params
            )
            response.raise_for_status()

            data = response.json()

            # Check for API errors
            if data.get("errors"):
                errors_str = ", ".join(data["errors"])
                raise ValueError(f"GNews API errors: {errors_str}")

            # Parse articles
            articles = [
                Article(
                    title=article["title"],
                    description=article.get("description"),
                    url=article["url"],
                    image=article.get("image"),
                    source=article["source"]["name"],
                    publishedAt=article["publishedAt"],
                )
                for article in data.get("articles", [])
            ]

            return SearchResult(
                totalArticles=data.get("totalArticles", 0), articles=articles
            )

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise ValueError("Invalid API key. Please check your GNEWS_API_KEY.")
        elif e.response.status_code == 429:
            raise ValueError(
                "API rate limit exceeded. Please try again later."
            )
        else:
            raise ValueError(f"API request failed: {e.response.status_code}")
    except httpx.TimeoutException:
        raise ValueError("API request timed out. Please try again.")
    except Exception as e:
        raise ValueError(f"Failed to get top headlines: {str(e)}")


# def main():
#     """Run the GNews MCP server"""
#     if not GNEWS_API_KEY:
#         print(
#             "Warning: GNEWS_API_KEY environment variable not set."
#         )
#         print(
#             "You can get a free API key at https://gnews.io"
#         )
#         print(
#             "Set it with: export GNEWS_API_KEY='your-api-key'"
#         )

#     mcp.run(transport="streamable-http")
#     # mcp.run(transport="stdio") --- IGNORE ---
