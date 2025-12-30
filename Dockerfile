# Dockerfile
FROM python:3.11-slim
WORKDIR /app

# install minimal system deps (for psycopg2)
RUN apt-get update && apt-get install -y build-essential libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# copy requirements and application
COPY requirements.txt /app/requirements.txt
COPY ./app /app/app
COPY ./alembic /app/alembic
COPY alembic.ini /app/alembic.ini
COPY start.sh /app/start.sh

# make start.sh executable
RUN chmod +x /app/start.sh

# install python deps
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8000
CMD ["/app/start.sh"]
