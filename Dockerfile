FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias para ultralytics/OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Instalar uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Instalar PyTorch CPU-only antes que ultralytics para evitar la versión CUDA
RUN uv pip install --system torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Copiar e instalar dependencias Python
COPY requirements-backend.txt .
RUN uv pip install --system -r requirements-backend.txt

# Copiar el código del backend
COPY app/ ./app/

# Descargar el modelo YOLO durante el build para no hacerlo en cada arranque
RUN python -c "from ultralytics import YOLO; YOLO('yolo26n.pt')"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
