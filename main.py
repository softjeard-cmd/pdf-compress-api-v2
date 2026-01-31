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
    # 1. Importación de seguridad
    import requests
    import os  # Necesario para medir el tamaño del archivo resultante
    
    # 2. Capturamos y mostramos los datos en el log
    data = await request.json()
    print("--- INICIANDO COMPRESIÓN DESDE GPT ---")
    print(f"Datos recibidos: {data}") 
    
    # --- DEFINICIÓN DE VARIABLES POR DEFECTO ---
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

    # 3. Descarga con verificación
    try:
        print(f"Descargando desde OpenAI...")
        response = requests.get(download_url, timeout=30)
        if response.status_code != 200:
            print(f"Error de descarga: Status {response.status_code}")
            return {"error": "No se pudo descargar de OpenAI"}
        
        # --- NUEVA MEDICIÓN: TAMAÑO DE ENTRADA ---
        tamano_entrada_mb = len(response.content) / (1024 * 1024)
        print(f"TAMAÑO INICIAL: {tamano_entrada_mb:.2f} MB")

    except Exception as e:
        print(f"Excepción en descarga: {str(e)}")
        return {"error": f"Fallo de conexión: {str(e)}"}

    # 4. Proceso de guardado temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as input_tmp:
        input_tmp.write(response.content)
        input_path = input_tmp.name

    output_path = tempfile.mktemp(suffix=".pdf")

    # 5. Proceso de compresión
    try:
        print("Ejecutando comprimir_solo_imagenes_pdf...")
        
        comprimir_solo_imagenes_pdf(
            input_path, 
            output_path, 
            calidad_por_defecto, 
            escala_por_defecto
        )
        
        # --- NUEVA MEDICIÓN: TAMAÑO DE SALIDA ---
        if os.path.exists(output_path):
            tamano_salida_mb = os.path.getsize(output_path) / (1024 * 1024)
            ahorro = ((tamano_entrada_mb - tamano_salida_mb) / tamano_entrada_mb) * 100
            print(f"TAMAÑO FINAL: {tamano_salida_mb:.2f} MB")
            print(f"REDUCCIÓN: {ahorro:.1f}%")
        
        print("¡Compresión exitosa!")

  # --- AQUÍ VA EL BLOQUE DE RETORNO ACTUALIZADO ---
        # Este mensaje aparecerá en tus logs justo antes de que el archivo salga hacia GPT
        print(f"ENVIANDO RESPUESTA BINARIA: OPTIMIZADO_{file_name}")
        
        return FileResponse(
            path=output_path,
            media_type="application/pdf",
            filename=f"OPTIMIZADO_{file_name}",
            headers={
                "Content-Disposition": f"attachment; filename=OPTIMIZADO_{file_name}",
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
        # --- FIN DEL BLOQUE ACTUALIZADO ---

    except Exception as e:
        print(f"Error en lógica de compresión: {str(e)}")
        return {"error": f"Error interno al comprimir: {str(e)}"}
    finally:
        # 6. Limpieza
        if os.path.exists(input_path):
            os.remove(input_path)
            print("Limpieza de archivos temporales completada.")

#CODIGO 3 - JASMAS ME RENDIRÉ------------------------------------------
##OJO CODIGO DE PRUEBA -----CSC:0523------------------------------------
########################################################################
########################################################################3
# --- NUEVA FUNCIONALIDAD: ENVÍO MEDIANTE LINK DE DESCARGA (V2) ---
from fastapi.staticfiles import StaticFiles
import shutil
import uuid

# 1. Creamos una carpeta física en el servidor para alojar los archivos temporalmente
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# 2. Montamos la carpeta para que sea accesible vía URL
app.mount("/static-download", StaticFiles(directory=DOWNLOAD_DIR), name="static-download")

@app.post("/compress-v2")
async def compress_gpt_v2(request: Request):
    import requests
    
    # Reutilizamos tu lógica de rastreo (print) que tanto nos ha servido
    data = await request.json()
    print("--- INICIANDO COMPRESIÓN V2 (LINK) ---")
    
    calidad_por_defecto = 41
    escala_por_defecto = 0.60
    
    files = data.get("openaiFileIdRefs", [])
    if not files:
        return {"status": "error", "message": "No se recibió archivo"}

    file_info = files[0]
    download_url = file_info.get("download_link")
    file_name = file_info.get("name", "archivo.pdf")

    try:
        # Descarga
        response = requests.get(download_url, timeout=30)
        tamano_entrada_mb = len(response.content) / (1024 * 1024)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as input_tmp:
            input_tmp.write(response.content)
            input_path = input_tmp.name

        output_path = tempfile.mktemp(suffix=".pdf")

        # Compresión usando tu función original
        print(f"Ejecutando compresión para: {file_name}")
        comprimir_solo_imagenes_pdf(input_path, output_path, calidad_por_defecto, escala_por_defecto)
        
        # Medición
        tamano_salida_mb = os.path.getsize(output_path) / (1024 * 1024)
        ahorro = ((tamano_entrada_mb - tamano_salida_mb) / tamano_entrada_mb) * 100

        # --- CAMBIO CLAVE: GUARDAR Y GENERAR LINK ---
        # Generamos un nombre único para evitar conflictos
        unique_name = f"{uuid.uuid4()}_OPTIMIZADO_{file_name}"
        save_path = os.path.join(DOWNLOAD_DIR, unique_name)
        
        # Movemos el archivo de la carpeta temporal a la carpeta de descargas pública
        shutil.move(output_path, save_path)
        
        # Construimos la URL pública de tu servidor en Render
        public_url = f"https://pdf-compressor-api-osad.onrender.com/static-download/{unique_name}"
        
        print(f"¡ÉXITO! Link generado: {public_url}")

        # Devolvemos JSON, que GPT procesa mucho mejor que archivos binarios
        return {
            "status": "success",
            "message": "Archivo comprimido exitosamente",
            "info": {
                "nombre": file_name,
                "tamano_original": f"{tamano_entrada_mb:.2f} MB",
                "tamano_comprimido": f"{tamano_salida_mb:.2f} MB",
                "reduccion": f"{ahorro:.1f}%"
            },
            "url_descarga": public_url
        }

    except Exception as e:
        print(f"Error en V2: {str(e)}")
        return {"status": "error", "message": str(e)}
    finally:
        if 'input_path' in locals() and os.path.exists(input_path):
            os.remove(input_path)







