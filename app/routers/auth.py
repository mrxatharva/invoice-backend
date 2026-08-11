from fastapi import APIRouter

router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login(data: dict):

    if (
        data["username"] == "admin"
        and
        data["password"] == "admin123"
    ):

        return {

            "access_token": "invoice_ai_token"

        }

    return {

        "detail": "Invalid Credentials"

    }