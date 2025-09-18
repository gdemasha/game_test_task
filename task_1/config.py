"""Configuration for db creation and connection with postgres"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from pydantic import BaseSettings


class Base(DeclarativeBase):
    """ Base class for models """
    pass


class Config(BaseSettings):
    """ Settings to make a connection to Postgres db """
    DB_HOST: str
    DB_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @property
    def database_url(self):
        # postgresql+psycopg://user:password@host:port/db_name

        return (
            f'postgresql+psycopg://{self.POSTGRES_USER}:'
            f'{self.POSTGRES_PASSWORD}@'
            f'{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}'
        )

    @property
    def alchemy_engine(self):
        engine = create_engine(
            url=self.database_url,
            pool_pre_ping=True,
            pool_size=100,
            max_overflow=200
        )
        return engine

    class Config:
        env_file = '.env'


settings = Config()
