PYTHON = python3

pre-init:pip install poetry poetry install

init: database/utils.py
	python -c "from database.utils import create_db; create_db()"

run:
	gunicorn -b 0.0.0.0:3000 -k uvicorn.workers.UvicornWorker provider_a_main:api
	gunicorn -b 0.0.0.0:8443 -k uvicorn.workers.UvicornWorker provider_b_main:api
	gunicorn -b 0.0.0.0:9000 -k uvicorn.workers.UvicornWorker airflow:api