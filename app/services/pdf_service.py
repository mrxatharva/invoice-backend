import fitz
import os

def pdf_to_images(pdf_path, output_folder="temp_pages"):
    os.makedirs(output_folder, exist_ok=True)

    doc = fitz.open(pdf_path)
    image_paths = []

    for page_no in range(len(doc)):
        page = doc.load_page(page_no)

        pix = page.get_pixmap(dpi=300)

        image_path = os.path.join(
            output_folder,
            f"page_{page_no+1}.png"
        )

        pix.save(image_path)

        image_paths.append(image_path)

    doc.close()

    return image_paths