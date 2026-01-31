from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import FileResponse
import tempfile
import os

from pdf_compress import comprimir_solo_imagenes_pdf

app = FastAPI(
    title="PDF Compressor API",
    description="API para comprimir PDFs ajustando calidad y escala de imágenes",
    version="1.0.0"
)

@app.post("/compress", summary="Comprime un archivo PDF")
async def compress_pdf(
    file: UploadFile = File(..., description="Archivo PDF a comprimir"),
    calidad: int = Query(
        41,
        ge=1,
        le=100,
        description="Calidad de las imágenes (1–100)"
    ),
    escala: float = Query(
        0.6,
        ge=0.1,
        le=1.0,
        description="Escala de las imágenes (0.1–1.0)"
    )
):
    # Validación básica
    if not file.filename.lower().endswith(".pdf"):
        return {"error": "El archivo debe ser un PDF"}

    # Archivo PDF de entrada temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as input_tmp:
        input_tmp.write(await file.read())
        input_path = input_tmp.name

    # Archivo PDF de salida temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as output_tmp:
        output_path = output_tmp.name

    # Compresión del PDF
    comprimir_solo_imagenes_pdf(
        input_path,
        output_path,
        calidad,
        escala
    )

    return FileResponse(
        path=output_path,
        media_type="application/pdf",
        filename="PDF_OPTIMIZADO.pdf"
    )
















