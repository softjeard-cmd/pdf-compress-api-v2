import base64
import tempfile
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from pdf_compress import comprimir_solo_imagenes_pdf

app = FastAPI()

class CompressRequest(BaseModel):
    filename: str
    pdf_base64: str
    calidad: int = 41
    escala: float = 0.6

@app.post("/compress")
def compress_pdf(data: CompressRequest):

    # 1️⃣ Decodificar base64 → bytes reales
    try:
        pdf_bytes = base64.b64decode(data.pdf_base64)
    except Exception:
        return {"error": "Base64 inválido"}

    # 2️⃣ Guardar como PDF REAL
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        f.write(pdf_bytes)
        input_path = f.name

    # 3️⃣ Archivo de salida
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        output_path = f.name

    # 4️⃣ Compresión
    comprimir_solo_imagenes_pdf(
        input_path,
        output_path,
        data.calidad,
        data.escala
    )

    # 5️⃣ Responder PDF
    return FileResponse(
        output_path,
        media_type="application/pdf",
        filename="PDF_OPTIMIZADO.pdf"
    )









