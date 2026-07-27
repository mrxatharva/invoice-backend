from app.services.validation_service import validate_invoice

data = {
    "vendor_name": "DEMO Sliced Invoices",
    "invoice_number": "INV-3337",
    "invoice_date": "January 25, 2016",
    "gstin": "AZ 12345",
    "total_amount": "93.50"
}

print(validate_invoice(data))
