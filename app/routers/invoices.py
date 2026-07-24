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