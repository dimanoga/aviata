import uuid

from pydantic import BaseModel


class ResponseModel(BaseModel):
    search_id: uuid.UUID
