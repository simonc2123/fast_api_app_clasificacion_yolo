import io
import time
from ultralytics import YOLO
from PIL import Image

from app.schemas import DetectionResponse, Detection, BoundingBox


class YoloObjectDetection:
    # Inicializa el modelo YOLO con la ruta del archivo de pesos
    def __init__(self, model_path: str = 'yolo26n.pt'):
        self.model = YOLO(model_path)
        print(f"Modelo YOLO cargado desde: {model_path}")

    def predict(self, image_bytes: bytes) -> DetectionResponse:
        # Convierte los bytes de la imagen a un objeto PIL Image
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # Realizar la inferencia y medir el tiempo de inferencia
        start_time = time.time()
        # Realiza la inferencia utilizando el modelo YOLO y obtiene los resultados
        results = self.model(image)

        end_time = time.time()
        
        #Tiempo de inferencia en milisegundos
        inference_time = (end_time - start_time) * 1000

        detections = []
        for result in results:
            for box in result.boxes:
                x_min, y_min, x_max, y_max = box.xyxy[0].tolist()
                confidence = box.conf[0].item()
                class_id = int(box.cls[0].item())
                class_name = self.model.names[class_id]

                bounding_box = BoundingBox(
                    x_min=x_min,
                    y_min=y_min,
                    x_max=x_max,
                    y_max=y_max
                )
                
                detection = Detection(
                    class_name=class_name,
                    confidence=confidence,
                    bounding_box=bounding_box
                )
                
                detections.append(detection)

        inference_time = round(inference_time, 2)  # Redondear a 2 decimales
        return DetectionResponse(detections=detections, inference_time=inference_time)
