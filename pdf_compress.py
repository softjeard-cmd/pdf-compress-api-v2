import fitz  # PyMuPDF
import io
from PIL import Image


def comprimir_solo_imagenes_pdf(
    entrada,
    salida,
    calidad=41,
    escala=0.60
):
    doc = fitz.open(entrada)

    for page in doc:
        for img in page.get_images(full=True):
            xref = img[0]

            if calidad == 100 and escala == 1:
                continue

            try:
                base = doc.extract_image(xref)
                img_bytes = base["image"]

                img_pil = Image.open(io.BytesIO(img_bytes))

                if img_pil.width < 50 or img_pil.height < 50:
                    continue

                if img_pil.mode != "RGB":
                    img_pil = img_pil.convert("RGB")

                if escala < 1:
                    new_w = int(img_pil.width * escala)
                    new_h = int(img_pil.height * escala)
                    if new_w < 50 or new_h < 50:
                        continue

                    img_pil = img_pil.resize(
                        (new_w, new_h),
                        Image.LANCZOS
                    )

                buffer = io.BytesIO()
                img_pil.save(
                    buffer,
                    format="JPEG",
                    quality=calidad,
                    optimize=True,
                    subsampling=2
                )

                page.replace_image(xref, stream=buffer.getvalue())

            except Exception:
                continue

    doc.save(salida, garbage=4, deflate=True, clean=True)
    doc.close()






