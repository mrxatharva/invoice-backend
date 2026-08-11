from product_correction_service import correct_invoice_products


invoice_json = {

    "vendor_name": "Samsuddin",

    "items": [

        {
            "description": "Fqlash TamKPysh Button-"
        },

        {
            "description": "Z+c EXD Brash"
        },

        {
            "description": "PreshqyNqt. uniranngs qoo"
        },

        {
            "description": "PiPeZ+d.ExP-amd PseshqPIP"
        },

        {
            "description": "Plomber: Charg<"
        },

        {
            "description": "Hodnolics. ost Broytngn"
        }

    ]
}


result = correct_invoice_products(
    invoice_json
)


print("\n")
print("=" * 70)
print("PRODUCT CORRECTION TEST")
print("=" * 70)


for item in result["items"]:

    print("\nOCR:")
    print(item["original_description"])

    print("CORRECTED:")
    print(item["corrected_description"])

    print("METHOD:")
    print(item["correction_method"])

    print("CONFIDENCE:")
    print(item["correction_confidence"])

    print("-" * 70)

