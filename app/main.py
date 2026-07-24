from fastapi import FastAPI
from app.routers import search
from app.database import engine
from app import model
from app.routers import export
from app.routers import upload
from app.routers import dashboard
from app.routers import invoices
from app.routers import analytics

model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Invoice Extraction API",
    version="1.0.0"
)

app.include_router(search.router)
app.include_router(upload.router)
app.include_router(dashboard.router)
app.include_router(invoices.router)
app.include_router(export.router)
app.include_router(analytics.router)

@app.get("/")
def root():
    return {
        "message": "Invoice Extraction Backend Running"
    }