import json
import ollama

MODEL = "qwen2.5:1.5b"


def validate_text_fields(ocr_text, invoice_json):

    prompt = f"""
You are an OCR spelling correction assistant.

You are NOT extracting invoices.

You already have a JSON extracted by another AI.

Your ONLY task is to improve OCR spelling.

Rules:

- Return ONLY valid JSON.
- Keep the JSON structure exactly the same.
- Never change numbers.
- Never change dates.
- Never change invoice number.
- Never calculate totals.
- Never invent missing values.
- Correct only obvious OCR spelling mistakes.

OCR TEXT:

{ocr_text}

CURRENT JSON:

{json.dumps(invoice_json, indent=2)}
"""

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    output = response["message"]["content"]

    output = output.replace("```json", "")
    output = output.replace("```", "").strip()

    return json.loads(output)