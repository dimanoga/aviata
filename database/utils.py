from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from database.base import Base
from provider_a_main import logger
from settings import DBSettings

DBSettings().setup_db()


def create_db() -> None:
    from requests import Request
    engine = create_engine(DBSettings().url)
    if not database_exists(engine.url):
        logger.info('Creating database')
        create_database(engine.url)
        Base.metadata.create_all(engine)

    logger.info(database_exists(engine.url))


create_db()
