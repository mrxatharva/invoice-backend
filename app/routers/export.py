from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import model
from app.services.pdf_report import create_pdf
from fastapi.responses import FileResponse

import pandas as pd
import json

router = APIRouter(
    prefix="/export",
    tags=["Export"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/excel")
def export_excel(db: Session = Depends(get_db)):

    invoices = db.query(model.Invoice).all()

    rows = []

    for invoice in invoices:

        data = {}

        if invoice.extracted_json:
            try:
                data = json.loads(invoice.extracted_json)
            except (TypeError, json.JSONDecodeError):
                data = {}

        rows.append({
            "Invoice ID": invoice.id,
            "Vendor": data.get("vendor_name"),
            "Invoice Number": data.get("invoice_number"),
            "Invoice Date": data.get("invoice_date"),
            "GSTIN": data.get("gst_number", data.get("gstin")),
            "Amount": data.get("grand_total", data.get("total_amount")),
            "Status": invoice.status
        })

    df = pd.DataFrame(rows)

    filename = "invoice_report.xlsx"

    df.to_excel(filename, index=False)

    return FileResponse(
        filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=filename
    )

@router.get("/pdf")
def export_pdf(db: Session = Depends(get_db)):

    invoices = db.query(model.Invoice).all()

    rows = [[
        "ID",
        "Vendor",
        "Invoice",
        "Date",
        "Amount"
    ]]

    for invoice in invoices:

        data = {}

        if invoice.extracted_json:
            try:
                data = json.loads(invoice.extracted_json)
            except (TypeError, json.JSONDecodeError):
                data = {}

        rows.append([
            invoice.id,
            data.get("vendor_name"),
            data.get("invoice_number"),
            data.get("invoice_date"),
            data.get("grand_total", data.get("total_amount"))
        ])

    filename = "invoice_report.pdf"

    create_pdf(rows, filename)

    return FileResponse(
        filename,
        media_type="application/pdf",
        filename=filename
    )
