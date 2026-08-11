import ollama
import json


MODEL = "gemma3:4b"


def extract_invoice(ocr_text):

    prompt = f"""
You are an invoice extraction engine.

Extract information from OCR text.

IMPORTANT RULES:

- Return ONLY a valid JSON object.
- Do NOT use markdown.
- Do NOT wrap the JSON in ```json.
- Do NOT add comments.
- Do NOT explain anything.
- Do NOT invent values.
- Do NOT perform calculations.
- Do NOT output mathematical expressions.
- If a value is missing or uncertain, return null.
- Preserve OCR text exactly for item descriptions.
- Output must be parseable by Python json.loads().
- Every field must contain ONLY:
  string, number, null, array, object, or boolean.

Return exactly this schema:

{{
  "vendor_name": null,
  "invoice_number": null,
  "invoice_date": null,
  "phone": [],
  "gst_number": null,
  "pan_number": null,
  "items": [
    {{
      "description": "",
      "quantity": null,
      "rate": null,
      "amount": null
    }}
  ],
  "subtotal": null,
  "tax": null,
  "grand_total": null
}}

OCR TEXT:

{ocr_text}
"""

    response = ollama.chat(
    model=MODEL,
    format="json",
    options={
        "temperature": 0,
        "num_ctx": 8192
    },
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

    output = response["message"]["content"].strip()

    # Remove markdown if present
    output = output.replace("```json", "")
    output = output.replace("```", "").strip()

    try:
        return json.loads(output)

    

    except json.JSONDecodeError as e:
        return {
            "error": str(e),
            "raw_output": output
        }