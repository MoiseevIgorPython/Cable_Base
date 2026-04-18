from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = ''
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_NAME: str
    FIRST_SUPERUSER_EMAIL: str = "admin@admin.ru"
    FIRST_SUPERUSER_PASSWORD: str = "admin123"
    DB_ECHO: bool = False

    model_config = ConfigDict(
        env_file='../.env',
        extra="ignore")

    @property
    def async_database_url(self) -> str:
        """Get async database URL."""
        user_pass = f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
        host_db = f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_NAME}'
        return f'postgresql+asyncpg://{user_pass}@{host_db}'


settings = Settings()
