from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from uuid import UUID
from sqlmodel import Session
from Entities.OpportunityDTOs.jobs_entity import CreateJob, UpdateJob, ReadJob
from Services.Opportunities.jobs_service import JobService
from Settings.logging_config import setup_logging
from db import get_session

logger = setup_logging()

router = APIRouter(prefix="/Dijkstra/v1/jobs", tags=["Jobs"])


@router.post("/", response_model=ReadJob)
def create_job(job_create: CreateJob, session: Session = Depends(get_session)):
    service = JobService(session)
    logger.info(f"Creating Job: {job_create.title}")
    job = service.create_job(job_create)
    logger.info(f"Created Job with ID: {job.id}")
    return job


@router.get("/{job_id}", response_model=ReadJob)
def get_job(job_id: UUID, session: Session = Depends(get_session)):
    service = JobService(session)
    logger.info(f"Fetching Job with ID: {job_id}")
    return service.get_job(job_id)


@router.get("/", response_model=List[ReadJob])
def list_jobs(
    skip: int = 0,
    limit: int = 20,
    sort_by: str = Query("created_at", description="Field to sort by"),
    order: str = Query("desc", description="asc or desc"),
    title: Optional[str] = None,
    organization: Optional[UUID] = None,
    location: Optional[str] = None,
    location_type: Optional[str] = None,
    employment_type: Optional[str] = None,
    category: Optional[str] = None,
    session: Session = Depends(get_session),
):
    service = JobService(session)
    logger.info(
        f"Listing Jobs: skip={skip}, limit={limit}, sort_by={sort_by}, order={order}, "
        f"title={title}, organization={organization}, location={location}, "
        f"location_type={location_type}, employment_type={employment_type}, category={category}"
    )
    jobs = service.list_jobs(
        skip,
        limit,
        sort_by,
        order,
        title,
        organization,
        location,
        location_type,
        employment_type,
        category,
    )
    logger.info(f"Returned {len(jobs)} jobs")
    return jobs


@router.get("/autocomplete/", response_model=List[ReadJob])
def autocomplete_jobs(
    query: str,
    field: str = Query("title", description="Field to search against"),
    limit: int = 10,
    session: Session = Depends(get_session),
):
    service = JobService(session)
    logger.info(f"Autocomplete query='{query}' field='{field}' limit={limit}")
    return service.autocomplete_jobs(query, field, limit)


@router.put("/{job_id}", response_model=ReadJob)
def update_job(job_id: UUID, job_update: UpdateJob, session: Session = Depends(get_session)):
    service = JobService(session)
    logger.info(f"Updating Job ID: {job_id} with data: {job_update.dict(exclude_unset=True)}")
    return service.update_job(job_id, job_update)


@router.delete("/{job_id}", response_model=ReadJob)
def delete_job(job_id: UUID, session: Session = Depends(get_session)):
    service = JobService(session)
    logger.info(f"Deleting Job ID: {job_id}")
    message = service.delete_job(job_id)
    logger.info(message)
    return {"detail": message}
