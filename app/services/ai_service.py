import json
from urllib import response
from google import genai
from app.config import GEMINI_API_KEY


client = genai.Client(api_key=GEMINI_API_KEY)


def extract_invoice_data(raw_text: str):

    prompt = f"""
You are an invoice extraction assistant.

Extract the invoice information from the following OCR text.

Return ONLY valid JSON.

OCR TEXT:

{raw_text}
"""

    response = client.models.generate_content(
    model="gemini-flash-latest",
    contents=prompt,
    )
    print(response.text)
    text = response.text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)