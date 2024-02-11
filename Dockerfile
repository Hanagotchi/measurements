FROM python:3.11-slim-buster

WORKDIR /app

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

COPY requirements.txt ./

RUN pip install -r requirements.txt

EXPOSE 8080

COPY app/ ./

CMD ["sh", "-c", "uvicorn main:app --reload --host 0.0.0.0 --port 8080 & python main_rabbitmq.py"]