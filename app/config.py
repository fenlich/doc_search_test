from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@db:5432/posts"
    elasticsearch_url: str = "http://elasticsearch:9200"
    es_index: str = "posts"
    seed_csv_path: str = "data/posts.csv"
    search_limit: int = 20

settings = Settings()