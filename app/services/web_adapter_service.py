from typing import Dict, Any
import httpx
from bs4 import BeautifulSoup

class WebAdapterService:
    @staticmethod
    async def fetch_structured_data(url: str) -> Dict[str, Any]:
        """
        Fetches a website and extracts structured data using BeautifulSoup.
        """
        async with httpx.AsyncClient(follow_redirects=True) as client:
            try:
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()
                html = response.text
            except Exception as e:
                return {
                    "url": url,
                    "status": "error",
                    "error_message": str(e)
                }

        soup = BeautifulSoup(html, "html.parser")

        # Extract basic metadata
        title = soup.title.string if soup.title else ""
        meta_description = ""
        meta_tag = soup.find("meta", attrs={"name": "description"})
        if meta_tag:
            meta_description = meta_tag.get("content", "")

        # Extract headers
        headers = {
            "h1": [h.get_text(strip=True) for h in soup.find_all("h1")],
            "h2": [h.get_text(strip=True) for h in soup.find_all("h2")]
        }

        # Extract links (top 10 for brevity)
        links = []
        for a in soup.find_all("a", href=True)[:10]:
            links.append({
                "text": a.get_text(strip=True),
                "href": a["href"]
            })

        # Extract main text content (first 1000 characters)
        # Remove script and style elements
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        text = soup.get_text(separator=" ", strip=True)
        content_summary = text[:1000] + "..." if len(text) > 1000 else text

        return {
            "url": url,
            "status": "extracted",
            "title": title,
            "metadata": {
                "description": meta_description
            },
            "headers": headers,
            "links": links,
            "content_summary": content_summary
        }
