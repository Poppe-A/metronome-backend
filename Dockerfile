FROM python:3.8.3-slim-buster

COPY /requirements.txt /app/requirements.txt
WORKDIR /app
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
RUN pip install -r requirements.txt
COPY ./app /app
