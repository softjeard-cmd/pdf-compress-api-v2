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
    # directorio temporal
    with tempfile.TemporaryDirectory() as tmp:
        input_path = os.path.join(tmp, file.filename)
        output_path = os.path.join(tmp, "PDF_OPTIMIZADO.pdf")

        # guardar archivo de entrada
        with open(input_path, "wb") as f:
            f.write(await file.read())

        # comprimir
        comprimir_solo_imagenes_pdf(
            input_path,
            output_path,
            calidad,
            escala
        )

        # devolver PDF
        return FileResponse(
            output_path,
            media_type="application/pdf",
            filename="PDF_OPTIMIZADO.pdf"
        )


