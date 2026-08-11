import re


def validate_invoice(data):

    confidence = 0
    checks = []

    # ==========================================
    # 1. Vendor Name
    # ==========================================

    if data.get("vendor_name"):
        confidence += 15
        checks.append({
            "field": "vendor_name",
            "status": "valid"
        })
    else:
        checks.append({
            "field": "vendor_name",
            "status": "missing"
        })


    # ==========================================
    # 2. Invoice Number
    # ==========================================

    if data.get("invoice_number"):
        confidence += 15
        checks.append({
            "field": "invoice_number",
            "status": "valid"
        })
    else:
        checks.append({
            "field": "invoice_number",
            "status": "missing"
        })


    # ==========================================
    # 3. Invoice Date
    # ==========================================

    if data.get("invoice_date"):
        confidence += 15
        checks.append({
            "field": "invoice_date",
            "status": "valid"
        })
    else:
        checks.append({
            "field": "invoice_date",
            "status": "missing"
        })


    # ==========================================
    # 4. Phone Number
    # ==========================================

    phones = data.get("phone", [])

    if isinstance(phones, str):
        phones = [phones]

    valid_phone = False

    for phone in phones:

        if re.fullmatch(r"\d{10}", str(phone)):
            valid_phone = True
            break

    if valid_phone:

        confidence += 10

        checks.append({
            "field": "phone",
            "status": "valid"
        })

    else:

        checks.append({
            "field": "phone",
            "status": "missing_or_invalid"
        })


    # ==========================================
    # 5. PAN Number
    # ==========================================

    pan = data.get("pan_number")

    if pan:

        pan_pattern = r"^[A-Z]{5}[0-9]{4}[A-Z]$"

        if re.fullmatch(pan_pattern, str(pan)):

            confidence += 10

            checks.append({
                "field": "pan_number",
                "status": "valid"
            })

        else:

            checks.append({
                "field": "pan_number",
                "status": "invalid"
            })

    else:

        checks.append({
            "field": "pan_number",
            "status": "missing"
        })


    # ==========================================
    # 6. GST Number
    # ==========================================

    gst = data.get("gst_number")

    if gst:

        gst_pattern = (
            r"^[0-9]{2}"
            r"[A-Z]{5}"
            r"[0-9]{4}"
            r"[A-Z]"
            r"[A-Z0-9]{3}$"
        )

        if re.fullmatch(gst_pattern, str(gst)):

            confidence += 10

            checks.append({
                "field": "gst_number",
                "status": "valid"
            })

        else:

            checks.append({
                "field": "gst_number",
                "status": "invalid"
            })

    else:

        checks.append({
            "field": "gst_number",
            "status": "missing"
        })


    # ==========================================
    # 7. Items
    # ==========================================

    items = data.get("items", [])

    valid_items = 0

    for item in items:

        quantity = item.get("quantity")
        rate = item.get("rate")
        amount = item.get("amount")

        if (
            isinstance(quantity, (int, float))
            and isinstance(rate, (int, float))
            and isinstance(amount, (int, float))
        ):

            calculated = quantity * rate

            # Allow small floating-point difference
            if abs(calculated - amount) < 0.01:

                valid_items += 1


    if items and valid_items == len(items):

        confidence += 15

        checks.append({
            "field": "items",
            "status": "valid"
        })

    elif items:

        checks.append({
            "field": "items",
            "status": "partially_valid"
        })

    else:

        checks.append({
            "field": "items",
            "status": "missing"
        })


    # ==========================================
    # Final Status
    # ==========================================

    if confidence >= 80:

        status = "valid"

    elif confidence >= 50:

        status = "warning"

    else:

        status = "invalid"


    # ==========================================
    # Return Validation Result
    # ==========================================

    return {

        "confidence": confidence,

        "status": status,

        "checks": checks

    }

