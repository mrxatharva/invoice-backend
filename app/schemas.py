from pydantic import BaseModel
from typing import Optional



class InvoiceCreate(BaseModel):
    vendor_name: Optional[str] = None
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None
    gst_number: Optional[str] = None
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    total_amount: Optional[float] = None


class InvoiceResponse(BaseModel):
    id: int

    vendor_name: Optional[str]
    invoice_number: Optional[str]
    invoice_date: Optional[str]
    gst_number: Optional[str]

    subtotal: Optional[float]
    tax: Optional[float]
    total_amount: Optional[float]

    file_name: str
    original_file_name: str
    file_path: str
    file_type: str

    class Config:
        from_attributes = True

        