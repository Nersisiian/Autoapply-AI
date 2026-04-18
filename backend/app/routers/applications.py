from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import get_db
from ..models import Application
from ..schemas import ApplicationCreate, ApplicationResponse

router = APIRouter(prefix="/applications", tags=["applications"])

@router.post("/", response_model=ApplicationResponse)
def create_application(app_data: ApplicationCreate, db: Session = Depends(get_db)):
    application = Application(
        job_id=app_data.job_id,
        resume_id=app_data.resume_id,
        fit_score=app_data.fit_score,
        cover_letter=app_data.cover_letter,
        status="draft",
        applied_at=datetime.utcnow(),
        notes=app_data.notes
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application

@router.get("/", response_model=list[ApplicationResponse])
def list_applications(db: Session = Depends(get_db)):
    return db.query(Application).order_by(Application.created_at.desc()).all()

@router.patch("/{app_id}/status")
def update_status(app_id: int, status: str, db: Session = Depends(get_db)):
    app = db.query(Application).filter(Application.id == app_id).first()
    if not app:
        raise HTTPException(404, "Application not found")
    app.status = status
    db.commit()
    return {"message": "Status updated"}