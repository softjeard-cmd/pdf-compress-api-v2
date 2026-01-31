import fitz
import io
from PIL import Image

def comprimir_solo_imagenes_pdf(entrada, salida, quality=41, scale=0.6):
    doc = fitz.open(entrada)

    for page in doc:
        img_list = page.get_images(full=True)

        for img in img_list:
            xref = img[0]

            try:
                base = doc.extract_image(xref)
                img_bytes = base["image"]

                im = Image.open(io.BytesIO(img_bytes)).convert("RGB")

                # resize
                if scale < 1:
                    w = int(im.width * scale)
                    h = int(im.height * scale)
                    if w > 10 and h > 10:
                        im = im.resize((w, h), Image.LANCZOS)

                buf = io.BytesIO()
                im.save(buf, format="JPEG", quality=quality)

                doc.update_stream(xref, buf.getvalue())

            except Exception as e:
                print("IMG ERROR:", e)
                continue

    doc.save(salida)
    doc.close()




