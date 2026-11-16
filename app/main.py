from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas, llm_service
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Clinical Research Intake Structurer",
    description="API for extracting validated clinical trial eligibility criteria from unstructured notes.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/extract", response_model=schemas.IntakeRecordResponse)
def create_extraction(request: schemas.IntakeRequest, db: Session = Depends(get_db)):
    try:
        extracted = llm_service.extract_clinical_criteria(request.raw_text)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM extraction failed: {str(e)}")

    db_record = models.IntakeRecord(
        raw_text=request.raw_text,
        **extracted.model_dump()
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@app.get("/api/records", response_model=List[schemas.IntakeRecordResponse])
def list_records(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(models.IntakeRecord).order_by(models.IntakeRecord.id.desc()).offset(skip).limit(limit).all()
