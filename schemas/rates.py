from pydantic.main import BaseModel


class RatesSchema(BaseModel):
    title: str
    description: str