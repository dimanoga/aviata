import uuid
from contextlib import contextmanager
from typing import Iterator, List

import sqlalchemy.orm as so
from sqlalchemy import and_, create_engine
from sqlalchemy_utils import create_database, database_exists

from database.base import Session, metadata
from database.requests_model import Request, StatusEnum
from database.results_model import Results
from logger import logger
from settings import DBSettings

DBSettings().setup_db()


def create_db() -> None:
    engine = create_engine(DBSettings().url)
    if not database_exists(engine.url):
        logger.info('Creating database')
        create_database(engine.url)
        metadata.create_all(engine)


@contextmanager
def create_session(expire_on_commit: bool = False) -> Iterator[so.Session]:
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


async def create_search_request(search_id: uuid.UUID, status: StatusEnum) -> None:
    with create_session() as session:
        item = Request(search_id=search_id)
        if status:
            item.status = status.value
        session.add(item)


async def get_search_request(search_id: uuid.UUID) -> Request:
    with create_session() as session:
        obj = session.query(Request).filter(Request.search_id == search_id).first()
        return obj


async def update_search_request(search_id: uuid.UUID, data: List[dict]) -> None:
    with create_session() as session:
        item = session.query(Request).filter(Request.search_id == search_id).first()
        if item:
            item.status = StatusEnum.completed.value
            item.data = data

    logger.info(f'Successfully update row with search_id: {search_id}')


async def create_search_result(
    search_id: uuid.UUID, data: List[dict], currency: str
) -> None:
    with create_session() as session:
        obj = Results(search_id=search_id, data=data, currency=currency)
        session.add(obj)


async def get_search_result(search_id: uuid.UUID, currency: str) -> Results:
    with create_session() as session:
        obj = (
            session.query(Results)
            .filter(and_(Results.search_id == search_id, Results.currency == currency))
            .first()
        )
        return obj
