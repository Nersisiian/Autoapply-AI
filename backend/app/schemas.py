from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict, Any

# Resume
class ResumeUploadResponse(BaseModel):
    id: int
    filename: str
    parsed_data: Dict[str, Any]

# Job
class JobResponse(BaseModel):
    id: int
    external_id: str
    title: str
    company: str
    location: str
    description: str
    url: str
    source: str
    posted_date: Optional[datetime]
    fit_score: Optional[float] = None

# Application
class ApplicationCreate(BaseModel):
    job_id: int
    resume_id: int
    fit_score: float
    cover_letter: str
    notes: Optional[str] = None

class ApplicationResponse(BaseModel):
    id: int
    job_id: int
    resume_id: int
    fit_score: float
    cover_letter: str
    status: str
    applied_at: Optional[datetime]
    notes: Optional[str]
    created_at: datetime

# LLM
class CoverLetterRequest(BaseModel):
    job_id: int
    resume_id: int

class CoverLetterResponse(BaseModel):
    cover_letter: str
    explanation: str
    suggestions: List[str]

# Autopilot
class AutopilotConfigBase(BaseModel):
    resume_id: int
    is_active: bool = False
    fit_threshold: float = 70.0
    check_interval_minutes: int = 60
    max_applications_per_run: int = 5

class AutopilotConfigCreate(AutopilotConfigBase):
    pass

class AutopilotConfigUpdate(BaseModel):
    resume_id: Optional[int] = None
    is_active: Optional[bool] = None
    fit_threshold: Optional[float] = None
    check_interval_minutes: Optional[int] = None
    max_applications_per_run: Optional[int] = None

class AutopilotConfigResponse(AutopilotConfigBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None