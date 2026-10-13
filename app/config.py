from dotenv import load_dotenv
import os

load_dotenv()

def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


class Settings:
    DB_HOST: str = _require("DB_HOST")
    DB_PORT: int = int(_require("DB_PORT"))
    POSTGRES_DB: str = _require("POSTGRES_DB")
    POSTGRES_USER: str = _require("POSTGRES_USER")
    POSTGRES_PASSWORD: str = _require("POSTGRES_PASSWORD")
    PGADMIN_PORT: int = int(_require("PGADMIN_PORT"))
    PGADMIN_PASSWORD: str = _require("PGADMIN_PASSWORD")
    PGADMIN_EMAIL: str = _require("PGADMIN_EMAIL")

    DB_ECHO: bool = os.getenv("DB_ECHO", "false").lower() == "true"
    POOL_PRE_PING: bool = os.getenv("POOL_PRE_PING", "false").lower() == "true"
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "5"))
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "10"))

    @property
    def database_url(self) -> str:
        return (
            "postgresql+psycopg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
