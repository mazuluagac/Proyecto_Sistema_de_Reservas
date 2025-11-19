FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    --no-install-recommends \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# wait-for-it
RUN curl -sSL https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -o /wait-for-it.sh \
 && chmod +x /wait-for-it.sh

EXPOSE 5004

CMD ["sh", "-c", "/wait-for-it.sh mongodb_audit:27017 --timeout=30 --strict -- gunicorn --bind 0.0.0.0:5004 --workers 2 app:app"]
