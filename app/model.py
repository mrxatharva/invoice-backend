from sqlalchemy import Column, Integer, String, Text, Float
from app.database import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)

    file_name = Column(String, nullable=False)
    original_file_name = Column(String, nullable=True)

    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)

    raw_text = Column(Text, nullable=True)
    extracted_json = Column(Text, nullable=True)

    status = Column(String, default="uploaded")
    validation_status = Column(String, default="pending")
    confidence_score = Column(Float, default=0)