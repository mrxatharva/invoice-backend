import json
import ollama

def extract_invoice_data(raw_text: str):

    prompt = f"""
You are an invoice extraction assistant.

Extract only the following fields and return ONLY valid JSON.

Fields:
- vendor_name
- invoice_number
- invoice_date
- gstin
- total_amount

Invoice Text:
{raw_text}
"""

    response = ollama.chat(
    model="gemma3:4b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    options={
        "temperature": 0,
        "top_p": 0.9,
        "num_predict": 512
    }
)

    result = response["message"]["content"]

    # Remove markdown
    result = result.replace("```json", "").replace("```", "").strip()

    return json.loads(result)