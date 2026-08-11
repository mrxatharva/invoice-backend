from paddleocr import PaddleOCR
from app.services.pdf_service import pdf_to_images
from PIL import Image
import numpy as np

ocr = PaddleOCR(
    use_angle_cls=True,
    lang="en"
)


def extract_text(image_path):

    # Open image
    image = Image.open(image_path).convert("RGB")

    # Convert to numpy array
    image = np.array(image)

    # OCR
    result = ocr.ocr(image, cls=True)

    text = []
    confidences = []
    low_confidence = []

    if result and result[0]:

        for line in result[0]:

            word = line[1][0]
            conf = float(line[1][1])

            text.append(word)
            confidences.append(conf)

            if conf < 0.80:
                low_confidence.append({
                    "word": word,
                    "confidence": round(conf * 100, 2)
                })

    avg = (
        sum(confidences) / len(confidences)
        if confidences else 0
    )

    return {
        "text": "\n".join(text),
        "average_confidence": round(avg * 100, 2),
        "low_confidence": low_confidence
    }


def extract_text_from_pdf(pdf_path):

    pages = pdf_to_images(pdf_path)

    complete_text = []
    confidences = []
    low = []

    for page in pages:

        print("Processing:", page)

        result = extract_text(page)

        complete_text.append(result["text"])
        confidences.append(result["average_confidence"])
        low.extend(result["low_confidence"])

    avg = (
        sum(confidences) / len(confidences)
        if confidences else 0
    )

    return {
        "text": "\n".join(complete_text),
        "average_confidence": round(avg, 2),
        "low_confidence": low
    }