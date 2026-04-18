import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "AutoApply AI"
    database_url: str = "sqlite:///./data/app.db"
    secret_key: str = "change-me-in-production"
    openai_api_key: str = ""
    local_llm_url: str = "http://ollama:11434"  # Docker service name
    use_local_llm: bool = True
    embedding_model: str = "all-MiniLM-L6-v2"
    
    # Autopilot defaults
    default_check_interval_minutes: int = 30
    default_fit_threshold: float = 70.0
    default_max_applications_per_run: int = 5

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()