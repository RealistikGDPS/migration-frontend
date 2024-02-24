FROM python:3.12

ENV PYTHONUNBUFFERED=1
ENV USE_ENV_CONFIG=1

WORKDIR /app

COPY requirements/main.txt requirements.txt
RUN pip install -r requirements.txt

COPY scripts .
COPY migration_frontend .
COPY templates .
COPY static .

ENTRYPOINT [ "/app/scripts/run_frontend.sh" ]
