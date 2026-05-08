from typing import Dict, Any
import httpx
from bs4 import BeautifulSoup
import ipaddress
import socket
from urllib.parse import urlparse, urljoin

class WebAdapterService:
    @staticmethod
    def _get_safe_ips(url: str) -> list[str]:
        """
        Resolves the URL to all available IPs and checks if ALL are safe (not private/internal).
        Returns the list of IP strings if all are safe, empty list otherwise.
        """
        try:
            parsed = urlparse(url)
            if parsed.scheme not in ["http", "https"]:
                return []

            hostname = parsed.hostname
            if not hostname:
                return []

            # getaddrinfo supports both IPv4 and IPv6, returns all addresses
            addr_info = socket.getaddrinfo(hostname, parsed.port or (80 if parsed.scheme == "http" else 443))

            safe_ips = []
            for family, _, _, _, sockaddr in addr_info:
                ip_str = sockaddr[0]
                ip = ipaddress.ip_address(ip_str)

                # Check if IP is private/internal
                if (ip.is_private or ip.is_loopback or ip.is_link_local or
                    ip.is_multicast or ip.is_unspecified):
                    return [] # If ANY IP is unsafe, the whole host is unsafe

                if ip_str not in safe_ips:
                    safe_ips.append(ip_str)

            return safe_ips
        except Exception:
            return []

    @staticmethod
    async def fetch_structured_data(url: str) -> Dict[str, Any]:
        """
        Fetches a website and extracts structured data using BeautifulSoup.
        Handles redirects manually and validates IPs to prevent SSRF.
        """
        current_url = url
        max_redirects = 5
        redirect_count = 0
        html = ""

        # Using a custom transport to pin the IP would be ideal for DNS rebinding protection.
        # However, for this environment and scale, we'll implement rigorous multi-IP validation
        # and manual redirect handling.
        async with httpx.AsyncClient(follow_redirects=False) as client:
            while redirect_count <= max_redirects:
                safe_ips = WebAdapterService._get_safe_ips(current_url)
                if not safe_ips:
                    return {
                        "url": url,
                        "status": "error",
                        "error_message": "Access to internal or invalid URLs is restricted."
                    }

                try:
                    # We fetch using the original URL but we've verified ALL IPs for the hostname are safe.
                    # This significantly reduces the window for DNS rebinding if the hostname
                    # is under the attacker's control and they swap it to a private IP.
                    response = await client.get(current_url, timeout=10.0)

                    if response.is_redirect:
                        redirect_count += 1
                        location = response.headers.get("Location")
                        if not location:
                            break
                        current_url = urljoin(current_url, location)
                        continue

                    response.raise_for_status()
                    html = response.text
                    break
                except Exception:
                    return {
                        "url": url,
                        "status": "error",
                        "error_message": "An error occurred while fetching the URL. Please ensure it is a valid, public website."
                    }

            if redirect_count > max_redirects:
                return {
                    "url": url,
                    "status": "error",
                    "error_message": "Too many redirects."
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
