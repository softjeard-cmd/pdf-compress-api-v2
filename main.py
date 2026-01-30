from fastapi import FastAPI, UploadFile, File, Form, Body
from fastapi.responses import FileResponse
import tempfile
import os
import base64

# Asegúrate de que este archivo pdf_compress.py esté en la misma carpeta
from pdf_compress import comprimir_solo_imagenes_pdf

app = FastAPI()

@app.post("/compress")
async def compress_pdf(
    file: UploadFile = File(...),
    quality: int = Form(41),
    scale: float = Form(0.6)
):
    # 1. Crear archivo temporal para la entrada
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as input_tmp:
        content = await file.read()
        input_tmp.write(content)
        input_path = input_tmp.name

    # 2. Ruta para el archivo de salida
    output_path = tempfile.mktemp(suffix=".pdf")

    try:
        # 3. Ejecutar la lógica de compresión
        comprimir_solo_imagenes_pdf(
            input_path,
            output_path,
            quality,
            scale
        )

        # 4. Retornar el archivo procesado
        return FileResponse(
            output_path,
            media_type="application/pdf",
            filename="PDF_OPTIMIZADO.pdf"
        )

    except Exception as e:
        return {"error": f"Error al procesar el PDF: {str(e)}"}
    
    finally:
        # Limpieza: Eliminamos solo el archivo de entrada
        if os.path.exists(input_path):
            os.remove(input_path)
            
 #CODIGO PARTE 2 -A INCLUIDO BASE64

@app.post("/compress_base64")
async def compress_base64(data: dict = Body(...)):
    file_b64 = data["file_base64"]

    # 🔧 quitar prefijo data URL si viene
    if "," in file_b64:
        file_b64 = file_b64.split(",")[1]

    # 🔧 corregir padding base64 si falta
    missing_padding = len(file_b64) % 4
    if missing_padding:
        file_b64 += "=" * (4 - missing_padding)

    pdf_bytes = base64.b64decode(file_b64)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as input_tmp:
        input_tmp.write(pdf_bytes)
        input_path = input_tmp.name

    output_path = tempfile.mktemp(suffix=".pdf")

    try:
        comprimir_solo_imagenes_pdf(
            input_path,
            output_path,
            41,
            0.6
        )

        with open(output_path, "rb") as f:
            result_b64 = base64.b64encode(f.read()).decode()

        return {"file_base64": result_b64}

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)



