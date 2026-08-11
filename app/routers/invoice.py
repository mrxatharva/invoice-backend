import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import model

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_invoices(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    if page < 1:
        page = 1

    if limit < 1:
        limit = 10

    if limit > 100:
        limit = 100

    total = db.query(model.Invoice).count()

    offset = (page - 1) * limit

    invoices = (
        db.query(model.Invoice)
        .order_by(model.Invoice.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    def invoice_summary(invoice):
        try:
            extracted_data = json.loads(invoice.extracted_json or "{}")
        except (TypeError, json.JSONDecodeError):
            extracted_data = {}

        return {
            "id": invoice.id,
            "file_name": invoice.file_name,
            "original_file_name": invoice.original_file_name,
            "file_type": invoice.file_type,
            "status": invoice.status,
            "validation_status": invoice.validation_status,
            "confidence_score": invoice.confidence_score,
            "invoice_data": extracted_data,
        }

    return {
        "success": True,
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": (total + limit - 1) // limit,
        "invoices": [invoice_summary(invoice) for invoice in invoices]
    }

@router.get("/search")
def search_invoices(
    vendor_name: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(model.Invoice)

    if vendor_name:
        query = query.filter(
            model.Invoice.extracted_json.ilike(
                f"%{vendor_name}%"
            )
        )

    if status:
        query = query.filter(
            model.Invoice.status == status
        )

    invoices = (
        query
        .order_by(model.Invoice.id.desc())
        .all()
    )

    def invoice_summary(invoice):
        try:
            extracted_data = json.loads(invoice.extracted_json or "{}")
        except (TypeError, json.JSONDecodeError):
            extracted_data = {}
        return {
            "id": invoice.id,
            "file_name": invoice.file_name,
            "original_file_name": invoice.original_file_name,
            "status": invoice.status,
            "validation_status": invoice.validation_status,
            "confidence_score": invoice.confidence_score,
            "invoice_data": extracted_data,
        }

    return {
        "success": True,
        "count": len(invoices),
        "invoices": [invoice_summary(invoice) for invoice in invoices]
    }

@router.get("/{invoice_id}")
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db)
):
    invoice = db.query(model.Invoice).filter(model.Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    try:
        extracted_data = json.loads(invoice.extracted_json or "{}")
    except (TypeError, json.JSONDecodeError):
        extracted_data = {}

    return {
        "success": True,
        "invoice": {
            "id": invoice.id,
            "file_name": invoice.file_name,
            "original_file_name": invoice.original_file_name,
            "file_path": invoice.file_path,
            "file_type": invoice.file_type,
            "raw_text": invoice.raw_text,
            "status": invoice.status,
            "validation_status": invoice.validation_status,
            "confidence_score": invoice.confidence_score,
            "extracted_data": extracted_data,
        }
    }
