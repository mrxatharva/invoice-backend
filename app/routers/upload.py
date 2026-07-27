from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import json
from app.services.validation_service import validate_invoice
from app.database import SessionLocal
from app import model
from app.services.upload_service import save_uploaded_file
from app.services.ocr_service import extract_text, extract_text_from_pdf
from app.services.ai_service import extract_invoice_data

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def upload_invoice(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # Step 1: Save uploaded file
        file_info = save_uploaded_file(file)

        # Step 2: OCR
        raw_text = ""

        if file_info["file_type"] in [".jpg", ".jpeg", ".png"]:
            raw_text = extract_text(file_info["file_path"])

        elif file_info["file_type"] == ".pdf":
            raw_text = extract_text_from_pdf(file_info["file_path"])

        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format"
            )

        # Step 3: AI Extraction
        invoice_json = {}

        if raw_text.strip():
            try:
                invoice_json = extract_invoice_data(raw_text)
            except Exception as e:
                invoice_json = {
                    "error": str(e)
                }

        # Validate AFTER AI extraction
        validation = validate_invoice(invoice_json)

        # Step 4: Save to Database
        invoice = model.Invoice(
            file_name=file_info["saved_name"],
            original_file_name=file_info["original_name"],
            file_path=file_info["file_path"],
            file_type=file_info["file_type"],
            raw_text=raw_text,
            extracted_json=json.dumps(invoice_json),
            status="completed",

            validation_status=validation["status"],
            confidence_score=validation["confidence"]
        )

        db.add(invoice)
        db.commit()
        db.refresh(invoice)

        # Step 5: Response
        return {
            "success": True,
            "message": "Invoice processed successfully",
            "invoice_id": invoice.id,
            "file_name": invoice.file_name,
            "invoice_data": invoice_json
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )