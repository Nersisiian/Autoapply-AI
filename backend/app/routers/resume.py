from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Resume
from ..schemas import ResumeUploadResponse
from ..services.parser import parse_resume
from ..services.embedding import embedding_service
import os
import uuid
import PyPDF2
import docx

router = APIRouter(prefix="/resume", tags=["resume"])

UPLOAD_DIR = "/app/data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def extract_text_from_pdf(file_path: str) -> str:
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        text = " ".join(page.extract_text() for page in reader.pages if page.extract_text())
    return text

def extract_text_from_docx(file_path: str) -> str:
    doc = docx.Document(file_path)
    return "\n".join(para.text for para in doc.paragraphs)

@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    ext = file.filename.split(".")[-1].lower()
    if ext not in ["pdf", "docx", "txt"]:
        raise HTTPException(400, "Only PDF, DOCX, TXT allowed")
    
    file_id = uuid.uuid4().hex
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.{ext}")
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    if ext == "pdf":
        text = extract_text_from_pdf(file_path)
    elif ext == "docx":
        text = extract_text_from_docx(file_path)
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

    parsed = parse_resume(text)
    embedding = embedding_service.encode_single(text)

    resume = Resume(
        filename=file.filename,
        raw_text=text,
        parsed_data=parsed,
        embedding=embedding
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return ResumeUploadResponse(id=resume.id, filename=resume.filename, parsed_data=parsed)

@router.get("/{resume_id}", response_model=ResumeUploadResponse)
def get_resume(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(404, "Resume not found")
    return resume