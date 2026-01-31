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



##============================================================================================
##JAMAS ME RINDO==============CODIGO 1 RESPUESTA DEL BACK=====================================

from fastapi import Request # Asegúrate de añadir Request a tus imports de fastapi

@app.post("/debug-gpt")
async def debug_gpt(request: Request):
    # Esto captura TODO el JSON que envía GPT
    data = await request.json()
    
    # Se imprimirá en los logs de Render
    print("--- DATOS RECIBIDOS DESDE GPT ---")
    print(data) 
    print("---------------------------------")
    
    return {
        "status": "recibido",
        "data_preview": data
    }


##============================================================================================
##JAMAS ME RINDO==============CODIGO 2 RESPUESTA DEL BACK=====================================
# --- SECCIÓN NUEVA PARA GPT ACTIONS ---
import requests

@app.post("/compress-gpt")
async def compress_from_gpt(request: Request):
    """
    Ruta específica para GPT Actions que recibe un enlace de descarga,
    lo procesa localmente y devuelve el archivo comprimido.
    """
    data = await request.json()
    files = data.get("openaiFileIdRefs", [])
    
    if not files:
        return {"error": "No se recibió ningún archivo de OpenAI"}

    # Extraemos la información del primer archivo recibido
    file_info = files[0]
    download_url = file_info.get("download_link")
    file_name = file_info.get("name", "archivo.pdf")

    # 1. Descarga del archivo desde los servidores de OpenAI
    try:
        response = requests.get(download_url, timeout=30)
        if response.status_code != 200:
            return {"error": "No se pudo descargar el archivo de OpenAI"}
    except Exception as e:
        return {"error": f"Error de conexión al descargar: {str(e)}"}

    # 2. Creación de archivo temporal para la entrada
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as input_tmp:
        input_tmp.write(response.content)
        input_path = input_tmp.name

    # Ruta temporal para el archivo de salida
    output_path = tempfile.mktemp(suffix=".pdf")

    try:
        # 3. Ejecución de tu lógica de compresión original
        comprimir_solo_imagenes_pdf(
            input_path, 
            output_path, 
            quality=41, 
            scale=0.6
        )

        # 4. Respuesta con el archivo procesado
        return FileResponse(
            output_path,
            media_type="application/pdf",
            filename=f"OPTIMIZADO_{file_name}"
        )

    except Exception as e:
        return {"error": f"Error en la compresión: {str(e)}"}
    
    finally:
        # Limpieza del archivo temporal de entrada
        if os.path.exists(input_path):
            os.remove(input_path)







