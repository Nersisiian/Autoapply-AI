from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import AutopilotConfig
from ..schemas import AutopilotConfigUpdate, AutopilotConfigResponse
from ..services.autopilot_service import run_autopilot

router = APIRouter(prefix="/autopilot", tags=["autopilot"])

@router.get("/config", response_model=AutopilotConfigResponse)
def get_config(db: Session = Depends(get_db)):
    config = db.query(AutopilotConfig).first()
    if not config:
        config = AutopilotConfig(resume_id=0, is_active=False)
        db.add(config)
        db.commit()
        db.refresh(config)
    return config

@router.post("/config", response_model=AutopilotConfigResponse)
def update_config(update: AutopilotConfigUpdate, db: Session = Depends(get_db)):
    config = db.query(AutopilotConfig).first()
    if not config:
        config = AutopilotConfig(resume_id=0)
        db.add(config)
    for key, value in update.dict(exclude_unset=True).items():
        setattr(config, key, value)
    db.commit()
    db.refresh(config)
    return config

@router.post("/run")
def trigger_autopilot(db: Session = Depends(get_db)):
    run_autopilot(db)
    return {"message": "Autopilot run completed"}