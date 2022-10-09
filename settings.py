from pydantic import BaseSettings

from database.base import metadata
from sqlalchemy.engine import Engine, engine_from_config


class RequestSettings(BaseSettings):
    provider_a_url: str = 'http://localhost:3000'
    provider_b_url: str = 'http://localhost:8443'


class DBSettings(BaseSettings):
    """Указывем настройки подключения к бд"""
    user: str = 'postgres'
    password: str = 'postgres'
    url: str = f'postgresql://{user}:{password}@localhost:5432/aviata_db'
    connection_timeout: int = 30
    echo: bool = False

    class Config:
        env_prefix = 'DB_'

    def setup_db(self) -> None:
        metadata.bind = self.create_engine()

    def create_engine(self) -> Engine:
        return engine_from_config(
            {
                'url': self.url,
                "connect_args": {'connect_timeout': self.connection_timeout},
            },
            prefix="",
        )
