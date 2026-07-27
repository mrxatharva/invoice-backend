from app.services.ai_service import extract_invoice_data

sample = """
Vendor: ABC Pvt Ltd
Invoice Number: INV-001
Invoice Date: 16/07/2026
GSTIN: 27ABCDE1234F1Z5
Total Amount: 11800
"""

print(extract_invoice_data(sample))