from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_VERSION: str = 'v1'
    DB_HOST: str = "localhost"
    DB_NAME: str = ""
    DB_USER: str = ""
    DB_PASSWORD: str = ""

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


settings = Settings()
