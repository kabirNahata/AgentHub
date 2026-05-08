from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List

class Settings(BaseSettings):
    app_name: str = "AgentHub — Agent-Native Web Infrastructure"
    version: str = "0.1.0"
    debug: bool = False
    api_keys: List[str] = ["agenthub-dev-key-2024"]

    @field_validator("api_keys", mode="before")
    @classmethod
    def parse_api_keys(cls, v):
        if isinstance(v, str):
            return [key.strip() for key in v.split(",") if key.strip()]
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()