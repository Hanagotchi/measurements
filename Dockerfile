FROM python:3.8
WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

EXPOSE 8080

COPY app/ ./

CMD ["sh", "-c", "uvicorn main:app --reload --host 0.0.0.0 --port 8080 & python main_rabbitmq.py"]