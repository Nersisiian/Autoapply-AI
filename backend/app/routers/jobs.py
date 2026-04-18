from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Job, Resume
from ..schemas import JobResponse
from ..services.scraper import fetch_jobs
from ..services.embedding import embedding_service
from ..services.matcher import match_jobs_to_resume

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("/fetch")
def fetch_new_jobs(db: Session = Depends(get_db)):
    jobs_data = fetch_jobs(limit=20)
    count = 0
    for job_dict in jobs_data:
        existing = db.query(Job).filter(Job.external_id == job_dict["external_id"]).first()
        if not existing:
            embedding = embedding_service.encode_single(job_dict["description"])
            job = Job(**job_dict, embedding=embedding)
            db.add(job)
            count += 1
    db.commit()
    return {"message": f"Added {count} new jobs"}

@router.get("/", response_model=List[JobResponse])
def list_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).order_by(Job.created_at.desc()).all()
    return jobs

@router.get("/match/{resume_id}", response_model=List[JobResponse])
def match_jobs(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(404, "Resume not found")
    if not resume.embedding:
        raise HTTPException(400, "Resume has no embedding")
    matched = match_jobs_to_resume(db, resume_id, resume.embedding)
    return matched