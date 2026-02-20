from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = ''
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    model_config = ConfigDict(
        env_file='.env',
        extra="ignore")

    @property
    def async_database_url(self) -> str:
        """Get async database URL."""
        user_pass = f'{self.DB_USER}:{self.DB_PASSWORD}'
        host_db = f'{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        return f'postgresql+asyncpg://{user_pass}@{host_db}'


settings = Settings()
