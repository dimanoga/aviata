FROM python:3.7

RUN python -m pip install poetry
    poetry install

WORKDIR /aviata

ADD provider_a_main.py provider_a_main.py
ADD provider_b_main.py provider_b_main.py