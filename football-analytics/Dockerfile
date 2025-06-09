FROM python:3.9-slim

WORKDIR /app
# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*
# Instalar numpy primero con versión específica
RUN pip install numpy==1.24.4
# Copiar requirements e instalar el resto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
