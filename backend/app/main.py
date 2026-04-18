from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from .database import engine, Base, SessionLocal
from .routers import resume, jobs, applications, llm, autopilot
from .services.autopilot_service import run_autopilot
from .config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables
Base.metadata.create_all(bind=engine)

def autopilot_job():
    db = SessionLocal()
    try:
        run_autopilot(db)
    except Exception as e:
        logger.error(f"Autopilot job failed: {e}")
    finally:
        db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(
    autopilot_job,
    trigger=IntervalTrigger(minutes=settings.default_check_interval_minutes),
    id="autopilot",
    replace_existing=True
)

app = FastAPI(title="AutoApply AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume.router)
app.include_router(jobs.router)
app.include_router(applications.router)
app.include_router(llm.router)
app.include_router(autopilot.router)

@app.on_event("startup")
def start_scheduler():
    scheduler.start()
    logger.info("Scheduler started for autopilot.")

@app.on_event("shutdown")
def stop_scheduler():
    scheduler.shutdown()

@app.get("/")
def root():
    return {"message": "AutoApply AI API is running"}