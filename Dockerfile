FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias para ultralytics/OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias Python
COPY requirements-backend.txt .
RUN pip install --no-cache-dir -r requirements-backend.txt

# Copiar el código del backend
COPY app/ ./app/

# Descargar el modelo YOLO durante el build para no hacerlo en cada arranque
RUN python -c "from ultralytics import YOLO; YOLO('yolo26n.pt')"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
