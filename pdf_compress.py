import fitz  # PyMuPDF
import shutil

def comprimir_solo_imagenes_pdf(entrada, salida, calidad, escala):
    doc = fitz.open(entrada)

    if doc.page_count == 0:
        doc.close()
        raise ValueError("PDF de entrada sin páginas")

    imagenes_encontradas = False

    for page in doc:
        images = page.get_images(full=True)

        if not images:
            continue

        imagenes_encontradas = True

        for img in images:
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            pix = fitz.Pixmap(image_bytes)

            if pix.alpha:
                pix = fitz.Pixmap(pix, 0)

            pix = fitz.Pixmap(
                pix,
                matrix=fitz.Matrix(escala, escala)
            )

            new_bytes = pix.tobytes("jpeg", quality=calidad)
            doc.update_stream(xref, new_bytes)

    # 🔴 CLAVE ABSOLUTA
    if not imagenes_encontradas:
        doc.close()
        # No hay imágenes → devuelve el PDF original
        shutil.copyfile(entrada, salida)
        return

    # Guardar solo si el doc sigue teniendo páginas
    if doc.page_count == 0:
        doc.close()
        raise ValueError("El PDF resultante quedó sin páginas")

    doc.save(salida, garbage=4, deflate=True, clean=True)
    doc.close()





