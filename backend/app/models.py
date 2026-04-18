from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON, Boolean
from sqlalchemy.sql import func
from .database import Base

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    raw_text = Column(Text)
    parsed_data = Column(JSON)  # skills, experience, education
    embedding = Column(JSON)    # list of floats
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True)
    title = Column(String)
    company = Column(String)
    location = Column(String)
    description = Column(Text)
    url = Column(String)
    source = Column(String)  # indeed, linkedin, etc.
    posted_date = Column(DateTime)
    embedding = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer)
    resume_id = Column(Integer)
    fit_score = Column(Float)
    cover_letter = Column(Text)
    status = Column(String, default="draft")  # draft, applied, rejected, interview
    applied_at = Column(DateTime(timezone=True))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AutopilotConfig(Base):
    __tablename__ = "autopilot_config"
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=False)
    fit_threshold = Column(Float, default=70.0)
    check_interval_minutes = Column(Integer, default=60)
    max_applications_per_run = Column(Integer, default=5)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())