from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Job, Resume
from ..schemas import CoverLetterRequest, CoverLetterResponse
from ..services.llm_agent import generate_cover_letter

router = APIRouter(prefix="/llm", tags=["llm"])

@router.post("/cover-letter", response_model=CoverLetterResponse)
def create_cover_letter(req: CoverLetterRequest, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == req.job_id).first()
    resume = db.query(Resume).filter(Resume.id == req.resume_id).first()
    if not job or not resume:
        raise HTTPException(404, "Job or Resume not found")
    response = generate_cover_letter(job.description, resume.raw_text)
    return response