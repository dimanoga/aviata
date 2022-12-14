import enum

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import JSON, UUID

from database.base import Base


class StatusEnum(enum.Enum):
    pending = 'PENDING'
    completed = 'COMPLETED'


class Request(Base):
    __tablename__ = 'requests'
    search_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    status = Column(String, nullable=False, default=StatusEnum.pending.value)
    data = Column(JSON, nullable=True)

    __table_args__ = {'extend_existing': True}
