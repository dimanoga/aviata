import uuid
from typing import List, Optional

from pydantic.main import BaseModel
from pydantic.types import Json


class RequestSchema(BaseModel):
    search_id: uuid.UUID
    status: str
    data: Optional[List[dict]]

    class Config:
        orm_mode = True
