import uuid
from fastapi import BackgroundTasks, FastAPI

from database.requests_model import StatusEnum
from database.utils import create_search_result
from schemas.airflow import ResponseModel
from settings import RequestSettings
from utils.search_flights import get_flights, process_result

api = FastAPI()


@api.post('/search/', status_code=200, response_model=ResponseModel)
async def search_flight(background_tasks: BackgroundTasks):
    request_settings = RequestSettings()
    search_id = uuid.uuid4()
    background_tasks.add_task(process_result, search_id=search_id, url=request_settings.provider_a_url + '/search')
    background_tasks.add_task(process_result, search_id=search_id, url=request_settings.provider_b_url + '/search')
    create_search_result(search_id=search_id, status=StatusEnum.pending)
    return {'search_id': search_id}
