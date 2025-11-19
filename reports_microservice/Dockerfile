FROM python:3.10-slim

# Establecemos el directorio de trabajo
WORKDIR /app

# Instalación de dependencias del sistema para mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    --no-install-recommends \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Copiamos requirements e instalamos dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el proyecto
COPY . .

# wait-for-it
RUN curl -sSL https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -o /wait-for-it.sh \
 && chmod +x /wait-for-it.sh

EXPOSE 8001

CMD ["sh", "-c", "/wait-for-it.sh reservation-db:3306 --timeout=30 --strict -- python manage.py migrate --noinput && gunicorn reports_microservice.wsgi:application --bind 0.0.0.0:8001"]
