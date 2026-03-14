FROM python:3.9-slim

WORKDIR /app

# Instalar libgomp1 requerida por PyTorch CPU
RUN apt-get update && apt-get install -y libgomp1 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app

RUN pip install --upgrade pip && \
    pip install flask Pillow requests && \
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

COPY app.py /app

CMD ["python", "app.py"]
