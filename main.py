from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
import tempfile
import os
import requests

from pdf_compress import comprimir_solo_imagenes_pdf

app = FastAPI()

# -------- ENDPOINT ORIGINAL (Swagger / Postman multipart) --------

@app.post("/compress")
async def compress_pdf(
    file: UploadFile = File(...),
    calidad: int = 41,
    escala: float = 0.6
):
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


# -------- NUEVO ENDPOINT (compatible GPT tool JSON) --------

class UrlReq(BaseModel):
    file_url: str
    calidad: int = 41
    escala: float = 0.6


@app.post("/compress-from-url")
async def compress_from_url(req: UrlReq):

    r = requests.get(req.file_url)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as input_tmp:
        input_tmp.write(r.content)
        input_path = input_tmp.name

    output_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    output_path = output_tmp.name
    output_tmp.close()

    comprimir_solo_imagenes_pdf(
        input_path,
        output_path,
        req.calidad,
        req.escala
    )

    return FileResponse(
        output_path,
        media_type="application/pdf",
        filename="PDF_OPTIMIZADO.pdf"
    )


