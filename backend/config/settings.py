from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Eris Project"
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()