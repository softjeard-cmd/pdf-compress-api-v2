from fastapi import FastAPI, UploadFile, File, Form, Body
from fastapi.responses import FileResponse
import tempfile
import os
import base64

from pdf_compress import comprimir_solo_imagenes_pdf

app = FastAPI()

# ---------------------------------------------------
# ENDPOINT MULTIPART — PRUEBAS MANUALES / SWAGGER
# ---------------------------------------------------

@app.post("/compress")
async def compress_pdf(
    file: UploadFile = File(...),
    quality: int = Form(41),
    scale: float = Form(0.6)
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as input_tmp:
        content = await file.read()
        input_tmp.write(content)
        input_path = input_tmp.name

    output_path = tempfile.mktemp(suffix=".pdf")

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
            filename="PDF_OPTIMIZADO.pdf"
        )

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)


# ---------------------------------------------------
# ENDPOINT BASE64 — GPT ACTIONS
# ---------------------------------------------------

@app.post("/compress_base64")
async def compress_base64(data: dict = Body(...)):

    input_path = None
    output_path = None

    try:
        file_b64 = data["file_base64"]
        quality = data.get("quality", 41)
        scale = data.get("scale", 0.6)

        # 🔧 quitar prefijo data URL si existe
        if "," in file_b64:
            file_b64 = file_b64.split(",")[1]

        # 🔧 corregir padding
        missing_padding = len(file_b64) % 4
        if missing_padding:
            file_b64 += "=" * (4 - missing_padding)

        pdf_bytes = base64.b64decode(file_b64)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as input_tmp:
            input_tmp.write(pdf_bytes)
            input_path = input_tmp.name

        output_path = tempfile.mktemp(suffix=".pdf")

        # 🔧 compresión segura con fallback
        try:
            comprimir_solo_imagenes_pdf(
                input_path,
                output_path,
                quality,
                scale
            )
        except Exception:
            # devolver original si falla compresión
            with open(input_path, "rb") as f:
                result_b64 = base64.b64encode(f.read()).decode()

            return {
                "filename": "PDF_ORIGINAL.pdf",
                "mime_type": "application/pdf",
                "data_base64": result_b64
            }

        # 🔧 si no generó salida → devolver original
        if not os.path.exists(output_path):
            with open(input_path, "rb") as f:
                result_b64 = base64.b64encode(f.read()).decode()

            return {
                "filename": "PDF_ORIGINAL.pdf",
                "mime_type": "application/pdf",
                "data_base64": result_b64
            }

        with open(output_path, "rb") as f:
            result_b64 = base64.b64encode(f.read()).decode()

        return {
            "filename": "PDF_OPTIMIZADO.pdf",
            "mime_type": "application/pdf",
            "data_base64": result_b64
        }

    except Exception as e:
        return {
            "error": str(e)
        }

    finally:
        if input_path and os.path.exists(input_path):
            os.remove(input_path)
        if output_path and os.path.exists(output_path):
            os.remove(output_path)






