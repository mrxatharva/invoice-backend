from rapidfuzz import fuzz, process


# ============================================================
# PRODUCT MASTER
# ============================================================
#
# Correct product name -> known OCR variations
#
# IMPORTANT:
# Only add aliases that you have verified.
# ============================================================

PRODUCT_MASTER = {

    "Flash Tank Push Button": [
        "Fqlash TamKPysh Button-",
        "Fqlsh TamKPysh Button",
        "Flash Tamk Push Button"
    ],

    "Z+C E.D. Brush": [
        "Z+c EXD Brash",
        "Z+c Brash",
        "Z+C ED Brush"
    ],

    "Pressure Nut Unions": [
        "PreshqyNqt. uniranngs",
        "PreshqyNqt. uniranngs qoo"
    ],

    "Pipe Z+D Exp. and Pressure Pipe": [
        "PiPeZ+d.ExP-amd PseshqPIP"
    ],

    "Plumber Charge": [
        "Plomber: Charg<"
    ],

    "Hydraulics and Cost Bracket": [
        "Hodnolics. ost Broytngn"
    ]
}


# ============================================================
# BUILD SEARCH LIST
# ============================================================

SEARCH_LIST = []

for correct_name, aliases in PRODUCT_MASTER.items():

    # Include the correct name
    SEARCH_LIST.append(
        (correct_name, correct_name)
    )

    # Include every known OCR alias
    for alias in aliases:

        SEARCH_LIST.append(
            (alias, correct_name)
        )


# ============================================================
# CORRECT PRODUCT NAME
# ============================================================

def correct_product_name(
    ocr_name,
    threshold=75
):

    if not ocr_name:

        return {
            "original": ocr_name,
            "corrected": None,
            "method": "none",
            "confidence": 0
        }


    # --------------------------------------------------------
    # Extract candidate strings
    # --------------------------------------------------------

    choices = [
        item[0]
        for item in SEARCH_LIST
    ]


    result = process.extractOne(
        ocr_name,
        choices,
        scorer=fuzz.WRatio
    )


    # --------------------------------------------------------
    # No match
    # --------------------------------------------------------

    if not result:

        return {
            "original": ocr_name,
            "corrected": None,
            "method": "manual_review",
            "confidence": 0
        }


    matched_text = result[0]
    score = result[1]


    # Find corresponding correct product
    corrected_product = None

    for search_text, correct_name in SEARCH_LIST:

        if search_text == matched_text:

            corrected_product = correct_name
            break


    # --------------------------------------------------------
    # Good match
    # --------------------------------------------------------

    if score >= threshold:

        return {
            "original": ocr_name,
            "corrected": corrected_product,
            "method": "fuzzy_match",
            "confidence": round(score, 2)
        }


    # --------------------------------------------------------
    # Weak match
    # --------------------------------------------------------

    return {
        "original": ocr_name,
        "corrected": None,
        "method": "manual_review",
        "confidence": round(score, 2)
    }


# ============================================================
# CORRECT ALL INVOICE ITEMS
# ============================================================

def correct_invoice_products(invoice_json):

    items = invoice_json.get("items", [])


    for item in items:

        ocr_name = item.get("description")


        result = correct_product_name(
            ocr_name
        )


        item["original_description"] = result["original"]

        item["corrected_description"] = result["corrected"]

        item["correction_method"] = result["method"]

        item["correction_confidence"] = result["confidence"]


    return invoice_json

