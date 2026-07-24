import easyocr

# Load the model only once when the application starts
reader = easyocr.Reader(["en"], gpu=False)


def extract_text(image_path: str) -> str:
    """
    Extract text from an image using EasyOCR.
    """

    result = reader.readtext(image_path, detail=0)

    return "\n".join(result)