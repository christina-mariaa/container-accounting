from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_PORT: int = 3306
    MYSQL_HOST: str = "db"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_EXPIRES_MIN: int = 15
    JWT_REFRESH_EXPIRES_DAYS: int = 30

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"mysql+asyncmy://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
            f"?charset=utf8mb4"
        )

    model_config = SettingsConfigDict(
        env_file=str(Path(".env")),
        extra="ignore",
    )


settings = Settings()
