import os
from typing import Any

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.tools import tool
from tavily import TavilyClient

load_dotenv()


def _get_tavily_client() -> TavilyClient:
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise RuntimeError(
            "TAVILY_API_KEY is missing. Add it to your .env file and restart Streamlit."
        )
    return TavilyClient(api_key=api_key)


@tool
def web_search(query: str) -> str:
    """Search the web for recent information and return titles, URLs, and snippets."""
    query = query.strip()
    if not query:
        return "Web search failed: query cannot be empty."
    try:
        response: dict[str, Any] = _get_tavily_client().search(
            query=query, max_results=5
        )
        results = response.get("results", [])
        if not results:
            return f"No web search results found for: {query}"
        output = []
        for result in results:
            output.append(
                "Title: {title}\nURL: {url}\nSnippet: {snippet}".format(
                    title=result.get("title", "Untitled"),
                    url=result.get("url", ""),
                    snippet=(result.get("content") or "").strip()[:500],
                )
            )
        return "\n\n----\n\n".join(output)
    except Exception as exc:
        return f"Web search failed: {type(exc).__name__}: {exc}"


@tool
def scrape_url(url: str) -> str:
    """Fetch a webpage and return cleaned readable text."""
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        return "Could not scrape URL: provide a valid http:// or https:// URL."
    try:
        response = requests.get(
            url,
            timeout=12,
            headers={"User-Agent": "Mozilla/5.0 (compatible; ResearchMind/1.0)"},
        )
        response.raise_for_status()
        content_type = response.headers.get("Content-Type", "").lower()
        if content_type and not any(
            kind in content_type
            for kind in ("text/html", "application/xhtml+xml")
        ):
            return f"Could not scrape URL: expected HTML, received {content_type}."
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(
            ["script", "style", "nav", "footer", "header", "noscript", "svg"]
        ):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)
        return text[:5000] if text else "Could not find readable text on that page."
    except requests.RequestException as exc:
        return f"Could not scrape URL: {type(exc).__name__}: {exc}"
    except Exception as exc:
        return f"Could not scrape URL: {type(exc).__name__}: {exc}"
