from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "AgentHub — Agent-Native Web Infrastructure"
    version: str = "0.1.0"
    debug: bool = False

settings = Settings()
