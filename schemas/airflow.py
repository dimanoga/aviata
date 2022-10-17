import uuid
from typing import List, Optional

from pydantic import BaseModel

from schemas.flights import FlightsModel


class ResponseModel(BaseModel):
    search_id: uuid.UUID


class PriceModel(BaseModel):
    amount: float
    currency: str


class FlightsResultModel(FlightsModel):
    price: Optional[PriceModel]


class SearchResultModel(ResponseModel):
    status: Optional[str]
    data: Optional[List[FlightsResultModel]]

    class Config:
        orm_mode = True
