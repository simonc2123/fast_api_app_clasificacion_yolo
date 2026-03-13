import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
import io

# Configuración de la página
st.set_page_config(page_title="Detección de Objetos con YOLO26n mas fastApi", layout="wide",
                   page_icon=":camera:")
st.title("Detección de Objetos con YOLO26n y FastAPI")
st.write("Sube una imagen para detectar objetos utilizando el modelo YOLO26n")

API_URL = "http://localhost:8000/api/v1/detect"
uploaded_file = st.file_uploader(
    "Selecciona una imagen (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # mostrar columnas para comparar imagen original con imagen procesada
    col1, col2 = st.columns(2)

    image = Image.open(uploaded_file).convert("RGB")
    with col1:
        st.header("Imagen Original")
        st.image(image, width='stretch')

    if st.button("Detectar Objetos"):
        with st.spinner("Detectando objetos..."):
            try:
                uploaded_file.seek(0)
                files = {"file": (uploaded_file.name,
                                  uploaded_file, uploaded_file.type)}
                response = requests.post(API_URL, files=files)
                response.raise_for_status()
                data = response.json()

                detections = data.get("detections", [])
                inference_time = data.get("inference_time", 0)

                # Dibujar las detecciones en la imagen
                image_draw = image.copy()
                draw = ImageDraw.Draw(image_draw)
                font = ImageFont.load_default()

                for det in detections:
                    bbox = det["bounding_box"]
                    x_min, y_min = bbox["x_min"], bbox["y_min"]
                    x_max, y_max = bbox["x_max"], bbox["y_max"]
                    label = f"{det['class_name']} {det['confidence']:.0%}"

                    draw.rectangle(
                        [(x_min, y_min), (x_max, y_max)], outline="red", width=3)
                    draw.rectangle(
                        [(x_min, y_min - 14), (x_min + len(label) * 7, y_min)], fill="red")
                    draw.text((x_min + 2, y_min - 13),
                              label, fill="white", font=font)

                with col2:
                    st.header("Detecciones")
                    st.image(image_draw, width='stretch')

                st.success(
                    f"✅ {len(detections)} objeto(s) detectado(s) en {inference_time:.2f} ms")

                if detections:
                    with st.expander("Ver detalle de detecciones"):
                        for i, det in enumerate(detections):
                            st.write(
                                f"**{i+1}. {det['class_name']}** — confianza: {det['confidence']:.2%}")
                else:
                    st.info("No se detectaron objetos en la imagen.")

            except requests.exceptions.ConnectionError:
                st.error(
                    "❌ No se pudo conectar al backend. Asegúrate de que esté corriendo en http://localhost:8000")
            except requests.exceptions.HTTPError as e:
                st.error(
                    f"❌ Error del servidor: {e.response.status_code} — {e.response.text}")
            except Exception as e:
                st.error(f"❌ Error inesperado: {str(e)}")
