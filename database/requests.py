import enum

from database.base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column


class StatusEnum(enum.Enum):
    pending = 'PENDING'
    completed = 'COMPLETED'


class Request(Base):
    __tablename__ = 'requests'
    request_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    status = Column(StatusEnum, nullable=False, default=StatusEnum.pending)
