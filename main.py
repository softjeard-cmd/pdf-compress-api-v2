from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
import tempfile
import os

# Asegúrate de que este archivo pdf_compress.py esté en la misma carpeta
from pdf_compress import comprimir_solo_imagenes_pdf

app = FastAPI()

@app.post("/compress")
async def compress_pdf(
    file: UploadFile = File(...),
    quality: int = Form(41),
    scale: float = Form(0.6)
):
    """
    Recibe un PDF y parámetros de compresión a través de un formulario multipart.
    """
    # 1. Crear archivo temporal para la entrada
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as input_tmp:
        content = await file.read()
        input_tmp.write(content)
        input_path = input_tmp.name

    # 2. Definir ruta para el archivo de salida
    # Usamos mktemp para tener una ruta válida pero el archivo lo crea la función de compresión
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
        # Limpieza: Eliminamos el archivo de entrada
        if os.path.exists(input_path):
            os.remove(input_path)
        # Nota: El archivo de salida lo gestiona FileResponse, 
        # para borrarlo automáticamente tras el envío se requeriría un BackgroundTask.




