from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, JSON

from database.base import Base


class Results(Base):
    __tablename__ = 'search_result'
    search_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    data = Column(JSON, nullable=True)

    __table_args__ = {'extend_existing': True}
