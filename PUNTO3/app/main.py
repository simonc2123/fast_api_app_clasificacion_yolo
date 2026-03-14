# backend usando fastapi
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException
from app.schemas import DetectionResponse
from app.yolo_service import YoloObjectDetection

ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Carga los modelos de ML al iniciar la aplicación
    ml_models['yolo'] = YoloObjectDetection(model_path='yolo26n.pt')
    yield
    # Ejecucion shutdown, si es necesario limpiar recursos o cerrar conexiones
    ml_models.clear()
    print("Modelos de ML limpiados y aplicación cerrada")


# instancia de la aplicación FastAPI con el contexto de vida útil definido
app = FastAPI(
    title="API de Detección de Objetos con YOLO",
    description="Una API para detectar objetos en imágenes utilizando el modelo YOLO 26s.",
    version="1.0.0",
    lifespan=lifespan
)


@app.post("/api/v1/detect", response_model=DetectionResponse, tags=["Detección de Objetos"])
async def detect_objects(file: UploadFile = File(...)) -> DetectionResponse:
    # Verificar que el archivo sea una imagen
    if file.content_type not in ("image/jpg", "image/jpeg", "image/png"):
        raise HTTPException(
            status_code=400, detail="El archivo debe ser una imagen en formato JPG, JPEG o PNG")

    try:
        # Leer los bytes de la imagen
        image_bytes = await file.read()
        # Obtener el modelo YOLO del diccionario de modelos
        yolo_model = ml_models.get('yolo')
        if yolo_model is None:
            raise HTTPException(
                status_code=500, detail="Modelo de detección no disponible")

        # Realizar la detección de objetos utilizando el modelo YOLO
        detection_response = yolo_model.predict(image_bytes)
        return detection_response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al procesar la imagen: {str(e)}")
