from pydantic_settings import BaseSettings

from typing import List
import os
api_keys: List[str] = os.getenv("API_KEYS", "").split(",")

class Settings(BaseSettings):
    app_name: str = "AgentHub — Agent-Native Web Infrastructure"
    version: str = "0.1.0"
    debug: bool = False
    api_keys: List[str] = api_keys

settings = Settings()
