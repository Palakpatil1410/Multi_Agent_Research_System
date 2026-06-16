from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic."""
    results = tavily.search(
    query=query,
    search_depth="advanced",
    max_results=5,
    include_answer=True
)

    out = []

    for r in results["results"]:
        out.append(
            f"Title: {r['title']}\n"
            f"URL: {r['url']}\n"
            f"Snippet: {r['content'][:300]}\n"
        )
        
    return "\n----\n".join(out)
    
@tool
def scrape_url(url : str) -> str:
    """Scrape the content of a web page and return the text."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, 'html.parser')
        for tag in soup(['script', 'style', 'nav', 'footer']):
            tag.decompose()
        return soup.get_text(separator='\n', strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
    


        
 