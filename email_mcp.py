"""
Email MCP Server - drafts dummy email from news articles
"""

from typing import List, Optional

from pydantic import BaseModel, Field

from mcp.server.fastmcp import FastMCP


# Initialize the FastMCP server
mcp = FastMCP(
    name="Email Server",
    instructions=(
        "Draft dummy email messages based on news data. "
        "Accepts output from GNews HTTP tools (search/get_top_headlines) "
        "and returns a JSON representation of the drafted email."
    ),
)


class Article(BaseModel):
    """News article model (mirrors GNews server definition)"""

    title: Optional[str] = Field(default=None, description="Article title")
    description: Optional[str] = Field(default=None, description="Article description")
    url: Optional[str] = Field(description="URL to the article")
    image: Optional[str] = Field(default=None, description="Image URL")


class SearchResult(BaseModel):
    """Container for search results coming from GNews tools"""

    totalArticles: Optional[int] = Field(default=None, description="Total number of articles found")
    articles: Optional[List[Article]] = Field(default=None, description="List of articles")


class EmailDraft(BaseModel):
    """Represents a very simple email draft"""

    to: str = Field(description="Recipient email address")
    subject: str = Field(description="Email subject line")
    body: str = Field(description="Plain text body of the email")


@mcp.tool()
async def draft_email(
) -> EmailDraft:
    """Create a dummy email draft given news articles.

    This tool is intended to be invoked after obtaining results from the
    GNews HTTP tools. It simply formats a subject and body and returns a
    JSON-serializable representation; no actual email sending is performed.

    Args:
        news: SearchResult object produced by gnews_http tools
        to: Recipient address (defaults to a placeholder)
        cc: Optional list of CC addresses
        bcc: Optional list of BCC addresses

    Returns:
        EmailDraft: JSON structure describing the drafted email
    """
    news = SearchResult(**data)  # ensure we have a proper SearchResult object
    subject = f"Top {news.totalArticles} news articles"
    # build a simple body listing the first few headlines and urls
    lines: List[str] = ["Hello,", "", "Here are some articles:", ""]
    for article in news.articles:
        lines.append(f"- {article.title}")
    lines.append("")
    lines.append("Links:")
    for article in news.articles:
        lines.append(article.url)
    lines.extend(["", "Regards,", "News Bot"])

    body = "\n".join(lines)

    return EmailDraft(to="adi@gmai.com", subject=subject, body=body)

# Dummy input (trimmed to match the user's provided JSON)
data = {
  "totalArticles": 2318,
  "articles": [
    {
      "title": "India and Brazil: Strengthening Ties in a Changing World",
      "description": "Indian Prime Minister Narendra Modi and Brazilian President Luiz Inacio Lula da Silva announced joint agreements on digital partnerships, rare earth cooperation, and mining collaboration. Lula praised mutual efforts for multilateral governance amidst shifting geopolitics during his state visit, highlighting, cultural, economic, and diplomatic synergies between the two nations.",
      "url": "https://www.devdiscourse.com/article/international/3812811-india-and-brazil-strengthening-ties-in-a-changing-world",
      "image": "https://www.devdiscourse.com/remote.axd?https://devdiscourse.blob.core.windows.net/devnews/21_02_2026_14_24_27_0754917.jpg?width=920&format=jpeg",
      "source": "Devdiscourse",
      "publishedAt": "2026-02-21T08:54:34Z"
    },
    {
      "title": "The new geopolitics of fashion: An Indian face on the cover of British Vogue",
      "description": "Fashion may appear trivial beside geopolitics. It is not. It encodes hierarchy long before policy debates catch up",
      "url": "https://indianexpress.com/article/opinion/columns/bhavitha-mandava-fashion-indian-face-on-the-cover-of-british-vogue-10544142/",
      "image": "https://images.indianexpress.com/2026/02/bhavitha-mandava-vogue-cover_20260221074207.png",
      "source": "The Indian Express",
      "publishedAt": "2026-02-21T07:45:34Z"
    },
    {
      "title": "ed is saying it's 'India's century'",
      "description": "US News: For years, 21st-century geopolitics has been framed as a heavyweight bout between Washington and Beijing. But what if the most consequential player is.",
      "url": "https://timesofindia.indiatimes.com/world/us/explained-5-reasons-why-nyt-op-ed-is-saying-its-indias-century/articleshow/128615244.cms",
      "image": "https://static.toiimg.com/thumb/msid-128621556,width-1280,height-720,imgsize-48778,resizemode-6,overlay-toi_sw,pt-32,y_pad-600/photo.jpg",
      "source": "Times of India",
      "publishedAt": "2026-02-20T19:02:00Z"
    },
    {
      "title": "Trump's China Odyssey: Trade Talks and Geopolitics",
      "description": "U.S. President Donald Trump's upcoming visit to China aims to navigate trade tensions and geopolitical issues. The meeting with Xi Jinping will address tariffs, fentanyl trade, and arms sales to Taiwan while exploring the extension of a trade truce, crucial for the world's biggest economies.",
      "url": "https://www.devdiscourse.com/article/headlines/3812246-trumps-china-odyssey-trade-talks-and-geopolitics",
      "image": "https://www.devdiscourse.com/remote.axd?https://devdiscourse.blob.core.windows.net/devnews/17_02_2026_11_38_13_4376289.jpg?width=920&format=jpeg",
      "source": "Devdiscourse",
      "publishedAt": "2026-02-20T15:33:17Z"
    },
    {
      "title": "London's FTSE indexes on track for weekly gains; geopolitics in focus",
      "description": "Britain's FTSE indexes gained on Friday and were set to end the week higher, led by defence stocks, while expectations for a March rate cut from the Bank of England and easing AI-disruption worries...",
      "url": "https://www.marketscreener.com/news/london-s-ftse-indexes-on-track-for-weekly-gains-geopolitics-in-focus-ce7e5ddddd8ff523",
      "image": "https://cdn.zonebourse.com/static/resize/0/0//images/reuters/2025-06/2025-06-26T114621Z_1_LYNXMPEL5P0MB_RTROPTP_4_VISMA-IPO.JPG",
      "source": "MarketScreener",
      "publishedAt": "2026-02-20T12:07:54Z"
    }
  ]
}