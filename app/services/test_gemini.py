from app.services.ai_service import extract_invoice_data

sample = """
ABC Pvt Ltd

Invoice No INV-001

Invoice Date 16/07/2026

GST 27ABCDE1234F1Z5

Total Amount 11800
"""

print(extract_invoice_data(sample))