import easyocr

from app.services.pdf_service import pdf_to_images

# Initialize EasyOCR only once
reader = easyocr.Reader(['en'], gpu=False)


def extract_text(image_path):
    """
    Extract text from an image using EasyOCR.
    """

    results = reader.readtext(image_path)

    text = ""

    for result in results:
        text += result[1] + "\n"

    return text.strip()


def extract_text_from_pdf(pdf_path):
    """
    Convert PDF pages to images and extract text from each page.
    """

    image_paths = pdf_to_images(pdf_path)

    full_text = ""

    for image in image_paths:

        page_text = extract_text(image)

        full_text += page_text + "\n\n"

    return full_text.strip()