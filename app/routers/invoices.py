from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Query
import json
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


# Get all invoices
@router.get("/")
def get_all_invoices(db: Session = Depends(get_db)):
    return db.query(model.Invoice).all()


# Search by vendor
@router.get("/vendor/{vendor_name}")
def search_vendor(vendor_name: str, db: Session = Depends(get_db)):
    return db.query(model.Invoice).filter(
        model.Invoice.extracted_json.contains(vendor_name)
    ).all()


# Search by status
@router.get("/status/{status}")
def search_status(status: str, db: Session = Depends(get_db)):
    return db.query(model.Invoice).filter(
        model.Invoice.status == status
    ).all()

@router.get("/search/")
def search_invoice(
    vendor: str = Query(None),
    status: str = Query(None),
    db: Session = Depends(get_db)
):

    invoices = db.query(model.Invoice).all()

    results = []

    for invoice in invoices:

        data = json.loads(invoice.extracted_json)

        if vendor:

            if vendor.lower() not in data.get(
                "vendor_name", ""
            ).lower():
                continue

        if status:

            if invoice.validation_status.lower() != status.lower():
                continue

        results.append({
            "id": invoice.id,
            "vendor": data.get("vendor_name"),
            "invoice_number": data.get("invoice_number"),
            "amount": data.get("total_amount"),
            "validation": invoice.validation_status,
            "confidence": invoice.confidence_score
        })

    return results

# Get invoice by ID
@router.get("/{invoice_id}")
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(model.Invoice).filter(
        model.Invoice.id == invoice_id
    ).first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    return invoice


# Delete invoice
@router.delete("/{invoice_id}")
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(model.Invoice).filter(
        model.Invoice.id == invoice_id
    ).first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    db.delete(invoice)
    db.commit()

    return {"message": "Invoice deleted successfully"}