from pydantic import BaseModel


class Settings(BaseModel):
    PROJECT_NAME: str = "Book Management API"

    SQLALACHEMY_DATABASE_URL: str = "sqlite:///./app.db"


settings = Settings()
