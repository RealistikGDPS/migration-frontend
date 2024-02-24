FROM python:3.12

ENV PYTHONUNBUFFERED=1
ENV USE_ENV_CONFIG=1

WORKDIR /app

COPY requirements/main.txt requirements.txt
RUN pip install -r requirements.txt

COPY migration_frontend .
COPY templates .
COPY static .

CMD ["uvicorn", "migration_frontend:main:asgi_app"]
