from typing import List
from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlmodel import Session

from Schema.jobs_schema import JobCreate, JobRead, JobUpdate
from Services.jobs_service import JobService
from Settings.logging_config import setup_logging
from db import get_session

logger = setup_logging()

router = APIRouter(prefix="/Dijkstra/v1/jobs", tags=["Jobs"])

@router.post("/", response_model=JobRead)
def create_job(job_create: JobCreate, session: Session = Depends(get_session)):
    service = JobService(session)
    return service.create_job(job_create)

@router.get("/{job_id}", response_model=JobRead)
def get_job(job_id: UUID, session: Session = Depends(get_session)):
    service = JobService(session)
    job = service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/", response_model=List[JobRead])
def list_jobs(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    service = JobService(session)
    return service.list_jobs(skip, limit)

@router.put("/{job_id}", response_model=JobRead)
def update_job(job_id: UUID, job_update: JobUpdate, session: Session = Depends(get_session)):
    service = JobService(session)
    job = service.update_job(job_id, job_update)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.delete("/{job_id}", response_model=JobRead)
def delete_job(job_id: UUID, session: Session = Depends(get_session)):
    service = JobService(session)
    job = service.delete_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
