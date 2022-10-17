PYTHON = python3
VENV = .venv
ALL = .
JOBS = 8

pre-init:pip install poetry poetry install

init: database/utils.py
	python -c "from database.utils import create_db; create_db()"

run:
	gunicorn -b 0.0.0.0:3000 -k uvicorn.workers.UvicornWorker provider_a_main:api
	gunicorn -b 0.0.0.0:8443 -k uvicorn.workers.UvicornWorker provider_b_main:api
	gunicorn -b 0.0.0.0:9000 -k uvicorn.workers.UvicornWorker airflow:api

pretty:
	$(VENV)/bin/isort $(ALL)
	$(VENV)/bin/black --skip-string-normalization $(ALL)

lint:
	$(VENV)/bin/black --skip-string-normalization --check $(ALL)
	$(VENV)/bin/flake8 --jobs $(JOBS) --statistics --show-source $(ALL)
	$(VENV)/bin/mypy $(ALL)

plint: pretty lint

