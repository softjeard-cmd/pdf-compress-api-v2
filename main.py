import httpx # Necesitarás instalar httpx: pip install httpx

@app.post("/compress")
async def compress_pdf(
    file_url: str = Form(...), # Ahora recibimos un link
    quality: int = Form(40),
    scale: float = Form(0.6)
):
    # 1. Descargar el archivo desde la URL que envía el GPT
    async with httpx.AsyncClient() as client:
        response = await client.get(file_url)
        if response.status_code != 200:
            return {"error": "No se pudo descargar el archivo del GPT"}
        pdf_content = response.content

    # 2. Guardar en temporal (el resto de tu lógica es igual)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as input_tmp:
        input_tmp.write(pdf_content)
        input_path = input_tmp.name

    output_path = tempfile.mktemp(suffix=".pdf")

    try:
        comprimir_solo_imagenes_pdf(input_path, output_path, quality, scale)
        return FileResponse(output_path, media_type="application/pdf", filename="PDF_OPTIMIZADO.pdf")
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)





