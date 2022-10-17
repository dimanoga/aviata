from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class Dep(BaseModel):
    at: str
    airport: str


class Arr(BaseModel):
    at: str
    airport: str


class Segment(BaseModel):
    operating_airline: str
    marketing_airline: str
    flight_number: str
    equipment: Optional[str]
    dep: Dep
    arr: Arr
    baggage: Any


class Flight(BaseModel):
    duration: int
    segments: List[Segment]


class Pricing(BaseModel):
    total: float
    base: float
    taxes: float
    currency: str


class FlightsModel(BaseModel):
    flights: List[Flight]
    refundable: bool
    validating_airline: str
    pricing: Pricing
