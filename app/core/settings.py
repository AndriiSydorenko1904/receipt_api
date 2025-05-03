from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/receipt_db"
    SQLALCHEMY_SYNC_URL: str = "postgresql://user:password@localhost:5432/receipt_db"
    SECRET_KEY: str = "0toMhKlJY3bcasfhFyihVjX_qZRa3A_SrfTMZh9xPUY"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
    RECEIPT_HEADER_NAME: str = "ФОП Джонсонюк Борис"


@lru_cache()
def get_settings():
    return Settings()
