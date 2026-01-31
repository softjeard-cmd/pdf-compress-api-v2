from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
import tempfile
import os

from pdf_compress import comprimir_solo_imagenes_pdf

app = FastAPI()

@app.post("/compress")
async def compress_pdf(
    file: UploadFile = File(...),
    quality: int = query(41),
    scale: float = query(0.6),
):
    # archivo de entrada
    input_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    input_path = input_tmp.name
    input_tmp.write(await file.read())
    input_tmp.close()

    # archivo de salida
    output_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    output_path = output_tmp.name
    output_tmp.close()

    try:
        comprimir_solo_imagenes_pdf(
            input_path,
            output_path,
            quality,
            scale
        )

        return FileResponse(
            output_path,
            media_type="application/pdf",
            filename="PDF_OPTIMIZED.pdf"
        )

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)










