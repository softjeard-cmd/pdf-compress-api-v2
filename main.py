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
@app.post("/compress-gpt")
async def compress_from_gpt(request: Request):
    # 1. Capturamos y mostramos los datos en el log
    data = await request.json()
    print("--- INICIANDO COMPRESIÓN DESDE GPT ---")
    print(f"Datos recibidos: {data}") 
    
    # --- DEFINICIÓN DE VARIABLES POR DEFECTO ---
    # Las definimos aquí para tener control total
    calidad_por_defecto = 41
    escala_por_defecto = 0.60
    print(f"Configuración: Calidad={calidad_por_defecto}, Escala={escala_por_defecto}")
    
    files = data.get("openaiFileIdRefs", [])
    if not files:
        print("ERROR: No se encontraron archivos en la petición")
        return {"error": "No se recibió ningún archivo de OpenAI"}

    file_info = files[0]
    download_url = file_info.get("download_link")
    file_name = file_info.get("name", "archivo.pdf")
    print(f"Procesando archivo: {file_name}")

    # 2. Descarga con verificación
    try:
        print(f"Descargando desde OpenAI...")
        response = requests.get(download_url, timeout=30)
        if response.status_code != 200:
            print(f"Error de descarga: Status {response.status_code}")
            return {"error": "No se pudo descargar de OpenAI"}
    except Exception as e:
        print(f"Excepción en descarga: {str(e)}")
        return {"error": "Fallo de conexión"}

    # 3. Proceso de compresión
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as input_tmp:
        input_tmp.write(response.content)
        input_path = input_tmp.name

    output_path = tempfile.mktemp(suffix=".pdf")

    try:
        print("Ejecutando comprimir_solo_imagenes_pdf...")
        
        # Llamamos a tu función asegurándonos de pasar los valores definidos arriba
        # Nota: Si tu función en pdf_compress.py usa nombres distintos, 
        # asegúrate de que coincidan (ej: calidad vs quality)
        comprimir_solo_imagenes_pdf(
            input_path, 
            output_path, 
            calidad_por_defecto, 
            escala_por_defecto
        )
        
        print("¡Compresión exitosa!")

        return FileResponse(
            output_path,
            media_type="application/pdf",
            filename=f"OPTIMIZADO_{file_name}"
        )
    except Exception as e:
        # Este print te dirá exactamente por qué falla la lógica interna ahora
        print(f"Error en lógica de compresión: {str(e)}")
        return {"error": f"Error interno al comprimir: {str(e)}"}
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
            print("Limpieza de archivos temporales completada.")




