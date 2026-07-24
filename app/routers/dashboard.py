from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import json

from app.database import SessionLocal
from app import model

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def dashboard(db: Session = Depends(get_db)):

    invoices = db.query(model.Invoice).all()

    total_amount = 0
    vendors = set()
    completed = 0
    failed = 0

    for invoice in invoices:

        if invoice.status == "completed":
            completed += 1
        else:
            failed += 1

        if invoice.extracted_json:

            data = json.loads(invoice.extracted_json)

            vendor = data.get("vendor_name")

            if vendor:
                vendors.add(vendor)

            amount = data.get("total_amount", 0)

            try:
                total_amount += float(amount)
            except:
                pass

    return {
        "total_invoices": len(invoices),
        "completed": completed,
        "failed": failed,
        "unique_vendors": len(vendors),
        "total_amount": total_amount
    }