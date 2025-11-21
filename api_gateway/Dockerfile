FROM python:3.12-slim

# Variables de sistema
ENV PYTHONUNBUFFERED=1 \
    #no generar archivos .pyc
    PYTHONDONTWRITEBYTECODE=1 \
    # no cachear paquetes instalados
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Instalar curl para healthcheck
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Puerto
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# Comando con Gunicorn para producción
CMD ["gunicorn", "--bind", "0.0.0.0:3000", "--workers", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "gateway:app"]