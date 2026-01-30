from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import tempfile
import os

from pdf_compress import comprimir_solo_imagenes_pdf

app = FastAPI()

@app.post("/compress")
async def compress_pdf(
    file: UploadFile = File(...),
    calidad: int = 41,
    escala: float = 0.6
):
    # archivo de entrada temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as input_tmp:
        input_tmp.write(await file.read())
        input_path = input_tmp.name

    # archivo de salida temporal
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




