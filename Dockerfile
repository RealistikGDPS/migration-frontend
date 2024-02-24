FROM python:3.12

ENV PYTHONUNBUFFERED=1
ENV USE_ENV_CONFIG=1

WORKDIR /app

COPY requirements/main.txt requirements.txt
RUN pip install -r requirements.txt

COPY scripts /app/scripts
COPY migration_frontend /app/migration_frontend
COPY templates /app/templates
COPY static /app/static

# Fix script permissions
RUN chmod +x /app/scripts/run_frontend.sh

ENTRYPOINT [ "/app/scripts/run_frontend.sh" ]
