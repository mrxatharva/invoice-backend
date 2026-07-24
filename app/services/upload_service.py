import os
import shutil
from pathlib import Path
from uuid import uuid4

UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg"
}


def save_uploaded_file(file):

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Only PDF, JPG, JPEG and PNG files are allowed."
        )

    unique_filename = f"{uuid4()}{extension}"

    file_path = os.path.join(
        UPLOAD_FOLDER,
        unique_filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "original_name": file.filename,
        "saved_name": unique_filename,
        "file_path": file_path,
        "file_type": extension
    }