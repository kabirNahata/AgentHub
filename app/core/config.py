from pydantic_settings import BaseSettings

from typing import List

class Settings(BaseSettings):
    app_name: str = "AgentHub — Agent-Native Web Infrastructure"
    version: str = "0.1.0"
    debug: bool = False
    api_keys: List[str] = ["agenthub-dev-key-2024", "secret-agent-key"]

settings = Settings()
