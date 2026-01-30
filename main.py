from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
import tempfile
import os

from pdf_compress import comprimir_solo_imagenes_pdf

app = FastAPI()


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/compress")
async def compress_pdf(
    file: UploadFile = File(...),
    quality: int = Form(41),
    scale: float = Form(0.6)
):
    try:
        # -------- guardar PDF entrada ----------
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as input_tmp:
            content = await file.read()
            input_tmp.write(content)
            input_path = input_tmp.name

        # -------- archivo salida ----------
        output_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        output_path = output_tmp.name
        output_tmp.close()

        # -------- comprimir ----------
        comprimir_solo_imagenes_pdf(
            input_path,
            output_path,
            quality,
            scale
        )

        # -------- devolver PDF ----------
        return FileResponse(
            output_path,
            media_type="application/pdf",
            filename="PDF_OPTIMIZADO.pdf"
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

    finally:
        if 'input_path' in locals() and os.path.exists(input_path):
            os.remove(input_path)


