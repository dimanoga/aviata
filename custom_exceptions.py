from http import HTTPStatus

from fastapi import HTTPException

SEARCH_NOT_FOUND = HTTPException(
    status_code=HTTPStatus.CONFLICT, detail='Search_id not found'
)
CURRENCY_NOT_FOUND = HTTPException(
    status_code=HTTPStatus.CONFLICT, detail='Currency not found'
)


class CurrencyNotFound(Exception):
    def __init__(self, message: str, code: int = HTTPStatus.NO_CONTENT):
        self.code = code
        self.message = message
