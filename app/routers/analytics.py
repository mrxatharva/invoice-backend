from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import model
import json

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def analytics(db: Session = Depends(get_db)):

    invoices = db.query(model.Invoice).all()

    amounts = []
    vendors = set()
    completed = 0
    failed = 0

    for invoice in invoices:

        if invoice.status == "completed":
            completed += 1
        else:
            failed += 1

        if invoice.extracted_json:

            try:
                data = json.loads(invoice.extracted_json)
            except (TypeError, json.JSONDecodeError):
                data = {}

            vendor = data.get("vendor_name")
            if vendor:
                vendors.add(vendor)

            try:
                amounts.append(float(data.get("grand_total", data.get("total_amount", 0)) or 0))
            except (TypeError, ValueError):
                pass

    return {
        "total_invoices": len(invoices),
        "completed": completed,
        "failed": failed,
        "unique_vendors": len(vendors),
        "total_amount": sum(amounts),
        "average_amount": sum(amounts) / len(amounts) if amounts else 0,
        "highest_invoice": max(amounts) if amounts else 0,
        "lowest_invoice": min(amounts) if amounts else 0
    }
