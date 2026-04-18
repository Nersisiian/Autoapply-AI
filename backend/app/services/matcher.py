import numpy as np
from ..models import Job
from sqlalchemy.orm import Session

def compute_fit_score(resume_embedding: list[float], job_embedding: list[float]) -> float:
    a = np.array(resume_embedding)
    b = np.array(job_embedding)
    cosine_sim = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return float(cosine_sim * 100)

def match_jobs_to_resume(db: Session, resume_id: int, resume_embedding: list[float]) -> list:
    jobs = db.query(Job).all()
    matched = []
    for job in jobs:
        if job.embedding:
            score = compute_fit_score(resume_embedding, job.embedding)
            job_dict = job.__dict__
            job_dict["fit_score"] = score
            matched.append(job_dict)
    matched.sort(key=lambda x: x["fit_score"], reverse=True)
    return matched