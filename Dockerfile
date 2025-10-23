FROM python:3.13-slim

# curl нужен для healthcheck внутри контейнера
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
