FROM python:3.8.3-slim-buster

COPY /requirements.txt /app/requirements.txt
COPY /run.py /run.py
COPY /app /app
RUN ls
WORKDIR /app
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
RUN pip install -r requirements.txt
CMD python ../run.py
