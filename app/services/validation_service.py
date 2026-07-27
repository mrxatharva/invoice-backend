import re


def validate_invoice(data):
    confidence = 0

    if data.get("vendor_name"):
        confidence += 20

    if data.get("invoice_number"):
        confidence += 20

    if data.get("invoice_date"):
        confidence += 20

    amount = data.get("total_amount")

    try:
        float(amount)
        confidence += 20
    except:
        pass

    gst = data.get("gstin")

    if gst:
        pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[A-Z0-9]{3}$'

        if re.match(pattern, gst):
            confidence += 20

    if confidence >= 80:
        status = "valid"
    elif confidence >= 50:
        status = "warning"
    else:
        status = "invalid"

    return {
        "confidence": confidence,
        "status": status
    }