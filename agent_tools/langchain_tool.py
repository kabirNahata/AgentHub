import httpx
from typing import Optional, Type
from pydantic import BaseModel, Field

class WebAdapterInput(BaseModel):
    url: str = Field(description="The URL of the website to adapt into structured JSON.")

# LangChain Tool Implementation
def get_agenthub_web_adapter_tool(base_url: str = "https://your-agenthub-url.com"):
    try:
        from langchain.tools import Tool
    except ImportError:
        raise ImportError("Please install langchain to use this tool wrapper: pip install langchain")

    async def run_adapter(url: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/api/v1/adapter/proxy", params={"url": url})
            return response.text

    return Tool(
        name="agenthub_web_adapter",
        description="Converts a human-facing website into clean, agent-readable JSON. Use this when you need to extract information from a website.",
        func=None, # LangChain's Tool typically expects sync, but can be used in async chains
        coroutine=run_adapter,
        args_schema=WebAdapterInput
    )
