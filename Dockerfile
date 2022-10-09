FROM python:3.7

RUN python -m pip install poetry gunicorn uvicorn

WORKDIR /aviata

COPY poetry.lock pyproject.toml req.txt /aviata/
RUN pip install -r req.txt

ADD provider_a_main.py provider_a_main.py
ADD provider_b_main.py provider_b_main.py

COPY . /aviata