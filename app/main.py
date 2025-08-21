from typing import List
from sqlmodel import Session
from fastapi import Depends, FastAPI, Request, HTTPException
from Settings.logging_config import setup_logging
from Entities.SearchParams import SearchParams
from app.Controllers import main_controller
from uuid import UUID

from Schema.jobs_schema import JobCreate, JobRead, JobUpdate
from Services.jobs_service import JobService
from app.Controllers import job_controller
from app.Controllers import certificate_controller
from db import get_session, init_db

app = FastAPI()

# Initialize logging
logger = setup_logging()

@app.on_event("startup")
def on_startup():
    logger.info("Starting up the application...")
    init_db()
    logger.info("Database initialized successfully.")

@app.on_event("shutdown")
def on_shutdown():
    logger.info("Shutting down the application...")

app.include_router(certificate_controller.router)
app.include_router(job_controller.router)