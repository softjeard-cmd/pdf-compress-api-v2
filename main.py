from fastapi import FastAPI, UploadFile, File, Form  # <--- PASO 1: Agrega 'Form' aquí
from fastapi.responses import FileResponse
import tempfile
import os

from pdf_compress import comprimir_solo_imagenes_pdf

app = FastAPI()

@app.post("/compress")
async def compress_pdf(
    file: UploadFile = File(...),
    calidad: int = Form(41),    # <--- PASO 2: Usa Form() para que coincida con el GPT
    escala: float = Form(0.6)   # <--- PASO 2: Usa Form() aquí también
):
    # El resto de tu código se queda exactamente igual
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as input_tmp:
        input_tmp.write(await file.read())
        input_path = input_tmp.name

    output_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    output_path = output_tmp.name
    output_tmp.close()

    comprimir_solo_imagenes_pdf(
        input_path,
        output_path,
        calidad,
        escala
    )

    return FileResponse(
        output_path,
        media_type="application/pdf",
        filename="PDF_OPTIMIZADO.pdf"
    )






