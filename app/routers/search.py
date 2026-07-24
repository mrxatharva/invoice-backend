from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import model

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

    invoices = db.query(model.Invoice).all()

    result = []

    for invoice in invoices:

        if vendor.lower() in (invoice.vendor_name or "").lower() and \
           invoice_number.lower() in (invoice.invoice_number or "").lower():

            result.append(invoice)

    return result