from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Therapist API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    SQLITE_URL: str = "sqlite:///./therapist.db"
    
    class Config:
        case_sensitive = True

settings = Settings()
