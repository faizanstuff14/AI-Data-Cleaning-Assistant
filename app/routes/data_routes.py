from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
import pandas as pd
import uuid
import os

from app.dependencies import get_current_user, get_db
from app.models import FileHistory, User
from app.cleaning.workflow import build_graph
from app.cleaning.report import generate_pdf

router = APIRouter(prefix="/data", tags=["Data"])
graph = build_graph()

os.makedirs("uploads", exist_ok=True)
os.makedirs("cleaned", exist_ok=True)


# UPLOAD & CLEAN CSV

@router.post("/upload")
def upload_csv(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    file_id = str(uuid.uuid4())

    raw_path = f"uploads/{file_id}.csv"
    clean_path = f"cleaned/{file_id}_clean.csv"
    pdf_path = f"cleaned/{file_id}_report.pdf"

    with open(raw_path, "wb") as f:
        f.write(file.file.read())

    try:
        df = pd.read_csv(raw_path, encoding="utf-8", engine="python")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid CSV file")

    if df.empty:
        raise HTTPException(status_code=400, detail="Uploaded CSV is empty")

    original_rows = len(df)

    state = {"df": df, "steps": []}
    final_state = graph.invoke(state)

    cleaned_df = final_state["df"]
    steps = final_state["steps"]

    cleaned_df.to_csv(clean_path, index=False)

    generate_pdf(
        pdf_path,
        file.filename,
        steps,
        original_rows,
        len(cleaned_df)
    )

    history = FileHistory(
        file_id=file_id,
        original_filename=file.filename,
        cleaned_csv_path=clean_path,
        pdf_report_path=pdf_path,
        user_id=current_user.id
    )
    db.add(history)
    db.commit()

    return {
        "message": "File cleaned successfully",
        "file_id": file_id,
        "steps": steps,
        "cleaned_csv": clean_path,
        "pdf_report": pdf_path
    }

#USER FILE HISTORY

@router.get("/history")
def get_upload_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    files = (
        db.query(FileHistory)
        .filter(FileHistory.user_id == current_user.id)
        .order_by(FileHistory.uploaded_at.desc())
        .all()
    )

    return [
        {
            "file_id": f.file_id,
            "original_filename": f.original_filename,
            "uploaded_at": f.uploaded_at,
            "cleaned_csv": f.cleaned_csv_path,
            "pdf_report": f.pdf_report_path,
        }
        for f in files
    ]

#DOWNLOAD CLEANED CSV

@router.get("/download/{file_id}")
def download_cleaned_csv(
    file_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    file = (
        db.query(FileHistory)
        .filter(
            FileHistory.file_id == file_id,
            FileHistory.user_id == current_user.id
        )
        .first()
    )

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file.cleaned_csv_path,
        filename=file.original_filename.replace(".csv", "_cleaned.csv"),
        media_type="text/csv"
    )
