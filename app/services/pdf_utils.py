import fitz
import os


def pdf_to_images(pdf_path, output_folder):
    images = []

    pdf = fitz.open(pdf_path)

    for page_no in range(len(pdf)):

        page = pdf.load_page(page_no)

        pix = page.get_pixmap(dpi=300)

        image_path = os.path.join(
            output_folder,
            f"page_{page_no + 1}.png"
        )

        pix.save(image_path)

        images.append(image_path)

    return images