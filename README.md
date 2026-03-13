# Clase FastAPI - Detección de Objetos con YOLO

API REST con FastAPI y frontend con Streamlit para detección de objetos en imágenes usando YOLO.

## Requisitos

- Python 3.12 o 3.13
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (gestor de paquetes)
- El archivo del modelo `yolo26n.pt` (ver sección abajo)

### Instalar `uv`

**Mac / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Obtener el modelo

El archivo `yolo26n.pt` no está incluido en el repositorio por ser un archivo binario.
Descargarlo y colocarlo en la raiz del proyecto (al mismo nivel que `pyproject.toml`).

## Instalacion

```bash
# Clonar el repositorio
git clone <url-del-repo>
cd clase-fastapi

# Instalar dependencias (crea el .venv automaticamente)
uv sync
```

## Correr el proyecto

### Opcion A - con Make (Mac / Linux)

```bash
# Backend (FastAPI en puerto 8000)
make backend

# Frontend (Streamlit) - en otra terminal
make frontend
```

### Opcion B - sin Make (Mac / Linux / Windows)

**Backend:**
```bash
uv run fastapi dev app/main.py --port 8000
```

**Frontend** (en otra terminal):
```bash
uv run streamlit run frontend/app.py
```

## Uso

- Backend API docs: http://localhost:8000/docs
- Frontend Streamlit: http://localhost:8501

## Estructura

```
clase-fastapi/
├── app/
│   ├── main.py          # FastAPI app y endpoints
│   ├── schemas.py       # Modelos Pydantic
│   └── yolo_service.py  # Logica de inferencia YOLO
├── frontend/
│   └── app.py           # Interfaz Streamlit
├── pyproject.toml       # Dependencias del proyecto
├── uv.lock              # Lockfile (reproducibilidad)
└── Makefile             # Comandos de conveniencia (Mac/Linux)
```
