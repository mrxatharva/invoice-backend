from app.services.ocr_service import extract_text

text = extract_text("sample.jpg")

print(text)