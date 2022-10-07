import uuid
from contextlib import contextmanager
from typing import Iterator, List
import sqlalchemy.orm as so
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from database.base import Session, metadata
from database.requests_schema import Request, StatusEnum
from logger import logger
from models.flights import FlightsModel
from settings import DBSettings

DBSettings().setup_db()


def create_db() -> None:
    engine = create_engine(DBSettings().url)
    if not database_exists(engine.url):
        logger.info('Creating database')
        create_database(engine.url)
        metadata.create_all(engine)


create_db()


@contextmanager
def create_session(expire_on_commit: bool = True) -> Iterator[so.Session]:
    """Provide a transactional scope around a series of operations."""
    new_session = Session(expire_on_commit=expire_on_commit)
    try:
        yield new_session
        new_session.commit()
    except Exception:
        new_session.rollback()
        raise
    finally:
        new_session.close()


def create_search_result(search_id: uuid.UUID, status: StatusEnum) -> None:
    with create_session() as session:
        item = Request(search_id=search_id)
        if status:
            item.status = status.value
        session.add(item)


def update_search_result(search_id: uuid.UUID, data: str) -> None:
    with create_session() as session:
        item = session.query(Request).filter(Request.search_id == search_id).first()
        item.status = StatusEnum.completed.value
        item.data = data

    logger.info(f'Successfully update row with search_id: {search_id}')
