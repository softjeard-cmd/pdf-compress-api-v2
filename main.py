import base64
import tempfile
from fastapi import FastAPI, HTTPException
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

    # ─────────────────────────────────────────────
    # PASO 1: BASE64 → BYTES (OBLIGATORIO)
    # ─────────────────────────────────────────────
    try:
        pdf_bytes = base64.b64decode(data.pdf_base64)
    except Exception:
        raise HTTPException(status_code=400, detail="Base64 inválido")

    # Validación mínima: ¿parece un PDF?
    if not pdf_bytes.startswith(b"%PDF"):
        raise HTTPException(status_code=400, detail="El archivo no es un PDF válido")

    # ─────────────────────────────────────────────
    # PASO 2: BYTES → ARCHIVO PDF REAL EN DISCO
    # (ESTO DEBE OCURRIR ANTES DE TODO)
    # ─────────────────────────────────────────────
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as input_tmp:
            input_tmp.write(pdf_bytes)
            input_pdf_path = input_tmp.name
    except Exception:
        raise HTTPException(status_code=500, detail="No se pudo escribir el PDF en disco")

    # ─────────────────────────────────────────────
    # A PARTIR DE AQUÍ, YA EXISTE UN PDF REAL
    # ─────────────────────────────────────────────

    # Archivo de salida
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as output_tmp:
        output_pdf_path = output_tmp.name

    # Paso siguiente (ya seguro)
    try:
        comprimir_solo_imagenes_pdf(
            input_pdf_path,
            output_pdf_path,
            data.calidad,
            data.escala
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al comprimir PDF: {str(e)}")

    return FileResponse(
        output_pdf_path,
        media_type="application/pdf",
        filename="PDF_OPTIMIZADO.pdf"
    )









