from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
import tempfile
import os

from pdf_compress import comprimir_solo_imagenes_pdf

app = FastAPI()

@app.post("/compress")
async def compress_pdf(
    file: UploadFile = File(...),
    quality: int = Form(41),
    scale: float = Form(0.6)
):
    with tempfile.TemporaryDirectory() as tmp:
        input_path = os.path.join(tmp, file.filename)
        output_path = os.path.join(tmp, "optimized.pdf")

        with open(input_path, "wb") as f:
            f.write(await file.read())

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





