from pydantic import BaseModel, Field
from typing import List


class BoundingBox(BaseModel):
    x_min: float = Field(...,
                         description="Coordenada x minima del cuadro delimitador")
    y_min: float = Field(...,
                         description="Coordenada y minima del cuadro delimitador")
    x_max: float = Field(...,
                         description="Coordenada x maxima del cuadro delimitador")
    y_max: float = Field(...,
                         description="Coordenada y maxima del cuadro delimitador")


class Detection(BaseModel):
    class_name: str = Field(
        ..., description="Nombre de la clase detectada (ejemplo: 'persona', 'auto')")
    confidence: float = Field(..., description="Confianza de la detección")
    bounding_box: BoundingBox = Field(...,
                                      description="Cuadro delimitador de la detección")


class DetectionResponse(BaseModel):
    detections: List[Detection] = Field(
        ..., description="Lista de detecciones encontradas en la imagen")
    inference_time: float = Field(
        ..., description="Tiempo que tomó realizar la inferencia en milisegundos")
