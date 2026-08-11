from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import model
import json

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def search(
    vendor: str = "",
    invoice_number: str = "",
    db: Session = Depends(get_db)
):

    invoices = db.query(model.Invoice).order_by(model.Invoice.id.desc()).all()
    result = []

    for invoice in invoices:
        try:
            data = json.loads(invoice.extracted_json or "{}")
        except (TypeError, json.JSONDecodeError):
            data = {}

        if (
            vendor.lower() in str(data.get("vendor_name") or "").lower()
            and invoice_number.lower() in str(data.get("invoice_number") or "").lower()
        ):
            result.append({
                "id": invoice.id,
                "file_name": invoice.file_name,
                "original_file_name": invoice.original_file_name,
                "status": invoice.status,
                "validation_status": invoice.validation_status,
                "confidence_score": invoice.confidence_score,
                "invoice_data": data,
            })

    return {"success": True, "count": len(result), "invoices": result}
