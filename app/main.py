from fastapi import FastAPI
from app.routers import search
from app.database import engine
from app import model
from app.routers import export
from app.routers import upload
from app.routers import dashboard
from app.routers import analytics
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth
from app.routers import invoice

model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Invoice Extraction API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(search.router)
app.include_router(upload.router)
app.include_router(dashboard.router)
app.include_router(export.router)
app.include_router(analytics.router)
app.include_router(auth.router)
app.include_router(invoice.router)

@app.get("/")
def root():
    return {
        "message": "Invoice Extraction Backend Running"
    }
