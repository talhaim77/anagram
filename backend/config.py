from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    API_VERSION: str = 'v1'
    DB_HOST: str = "localhost"
    DB_NAME: str = ""
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    CURRENT_FILE: str = Path(__file__)

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


settings = Settings()
