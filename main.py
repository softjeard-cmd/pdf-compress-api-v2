from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import FileResponse
import tempfile
import os

from pdf_compress import comprimir_solo_imagenes_pdf

app = FastAPI()


@app.post("/compress")
async def compress_pdf(
    file: UploadFile = File(...),
    quality: int = Query(41),
    scale: float = Query(0.6)
):
    # crear carpeta temporal segura
    with tempfile.TemporaryDirectory() as tmp:
        input_path = os.path.join(tmp, file.filename or "input.pdf")
        output_path = os.path.join(tmp, "optimized.pdf")

        # guardar archivo subido
        content = await file.read()
        with open(input_path, "wb") as f:
            f.write(content)

        # comprimir
        comprimir_solo_imagenes_pdf(
            input_path,
            output_path,
            quality,
            scale
        )

        # devolver PDF resultante
        return FileResponse(
            output_path,
            media_type="application/pdf",
            filename="PDF_OPTIMIZED.pdf"
        )









