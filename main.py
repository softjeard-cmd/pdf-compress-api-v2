from fastapi import FastAPI, UploadFile, File, Form # Añade Form
from fastapi.responses import FileResponse
import tempfile
import os

from pdf_compress import comprimir_solo_imagenes_pdf

app = FastAPI()

@app.post("/compress")
async def compress_pdf(
    file: UploadFile = File(...),
    calidad: int = Form(41),      # Cambia esto a Form
    escala: float = Form(0.6)     # Cambia esto a Form
):
    # El resto de tu código igual...
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as input_tmp:
        input_tmp.write(await file.read())
        input_path = input_tmp.name

    output_path = tempfile.mktemp(suffix=".pdf")

    try:
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
    finally:
        # Es buena práctica limpiar archivos temporales después de enviarlos
        # aunque con FileResponse a veces es mejor dejar que el sistema lo maneje
        if os.path.exists(input_path):
            os.remove(input_path)





