from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import json

from app.database import SessionLocal
from app import model

from app.services.upload_service import save_uploaded_file
from app.services.paddle_service import extract_text, extract_text_from_pdf
from app.services.gemma_service import extract_invoice
from app.services.validation_service import validate_invoice
from app.services.product_correction_service import correct_invoice_products

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


# ==========================================
# Database Dependency
# ==========================================

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ==========================================
# Upload Invoice
# ==========================================

@router.post("/")
def upload_invoice(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    try:

        # ==========================================
        # STEP 1 : Save Uploaded File
        # ==========================================

        file_info = save_uploaded_file(file)

        print("=" * 60)
        print("FILE SAVED")
        print(file_info)
        print("=" * 60)


        # ==========================================
        # STEP 2 : OCR
        # ==========================================

        if file_info["file_type"] in [
            ".jpg",
            ".jpeg",
            ".png"
        ]:

            ocr_result = extract_text(
                file_info["file_path"]
            )

        elif file_info["file_type"] == ".pdf":

            ocr_result = extract_text_from_pdf(
                file_info["file_path"]
            )

        else:

            raise HTTPException(
                status_code=400,
                detail="Unsupported file format"
            )


        # ==========================================
        # Get OCR Results
        # ==========================================

        raw_text = ocr_result["text"]

        confidence = ocr_result["average_confidence"]


        print("=" * 60)
        print("OCR FINISHED")
        print(f"Confidence : {confidence:.2f}%")
        print("=" * 60)


        # ==========================================
        # STEP 3 : Gemma Extraction
        # ==========================================

        print("=" * 60)
        print("RUNNING GEMMA EXTRACTION")
        print("=" * 60)

        invoice_json = extract_invoice(raw_text)

        # ======================================
        # STEP 3.5 : Product Name Correction
        # ======================================

        invoice_json = correct_invoice_products(
            invoice_json
        )


        print("=" * 60)
        print("GEMMA EXTRACTION FINISHED")
        print(invoice_json)
        print("=" * 60)


        # ==========================================
        # STEP 4 : Validation
        # ==========================================

        print("=" * 60)
        print("RUNNING VALIDATION")
        print("=" * 60)

        validation = validate_invoice(invoice_json)


        print("=" * 60)
        print("VALIDATION FINISHED")
        print(f"Validation confidence : {validation['confidence']}%")
        print(f"Validation status     : {validation['status']}")
        print("=" * 60)


        # ==========================================
        # STEP 5 : Save to Database
        # ==========================================

        invoice = model.Invoice(

            file_name=file_info["saved_name"],

            original_file_name=file_info["original_name"],

            file_path=file_info["file_path"],

            file_type=file_info["file_type"],

            raw_text=raw_text,

            extracted_json=json.dumps(
                invoice_json,
                indent=2
            ),

            status="completed",

            validation_status=validation["status"],

            confidence_score=confidence

        )


        db.add(invoice)

        db.commit()

        db.refresh(invoice)


        # ==========================================
        # STEP 6 : API Response
        # ==========================================

        return {

            "success": True,

            "message": "Invoice processed successfully",

            "invoice_id": invoice.id,

            "ocr_confidence": confidence,

            "ocr_engine": "PaddleOCR",

            "llm": "Gemma3",

            "validation": validation,

            "invoice_data": invoice_json

        }


    except HTTPException:

        raise


    except Exception as e:

        print("=" * 60)
        print("UPLOAD PROCESSING ERROR")
        print(str(e))
        print("=" * 60)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

