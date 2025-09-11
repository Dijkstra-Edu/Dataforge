from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from uuid import UUID
from sqlmodel import Session

from Settings.logging_config import setup_logging
from Entities.UserDTOs.workexperience_entity import CreateWorkExperience, ReadWorkExperience, ReadWorkExperienceWithRelations, UpdateWorkExperience
from Services.User.workexperience_service import WorkExperienceService
from db import get_session
from Schema.SQL.Enums.enums import EmploymentType, WorkLocationType, Domain

logger = setup_logging()

router = APIRouter(prefix="/Dijkstra/v1/wp", tags=["Work Experiences"])


@router.post("/", response_model=ReadWorkExperience)
def create_work_experience(work_experience_create: CreateWorkExperience, session: Session = Depends(get_session)):
    service = WorkExperienceService(session)
    logger.info(f"Creating Work Experience: {work_experience_create.title} at {work_experience_create.company_name}")
    try:
        work_experience = service.create_work_experience(work_experience_create)
        logger.info(f"Created Work Experience with ID: {work_experience.id}")
        return work_experience
    except ValueError as e:
        logger.warning(f"Failed to create work experience: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error creating work experience: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{work_experience_id}", response_model=ReadWorkExperienceWithRelations)
def get_work_experience(work_experience_id: UUID, session: Session = Depends(get_session)):
    service = WorkExperienceService(session)
    logger.info(f"Fetching Work Experience with ID: {work_experience_id}")
    work_experience = service.get_work_experience(work_experience_id)
    if not work_experience:
        logger.warning(f"Work Experience not found: {work_experience_id}")
        raise HTTPException(status_code=404, detail="Work Experience not found")
    return work_experience


@router.get("/profile/{profile_id}", response_model=List[ReadWorkExperience])
def get_work_experiences_by_profile_id(profile_id: UUID, session: Session = Depends(get_session)):
    service = WorkExperienceService(session)
    logger.info(f"Fetching Work Experiences for profile ID: {profile_id}")
    work_experiences = service.get_work_experiences_by_profile_id(profile_id)
    logger.info(f"Returned {len(work_experiences)} work experiences for profile {profile_id}")
    return work_experiences


@router.get("/", response_model=List[ReadWorkExperience])
def list_work_experiences(
    skip: int = 0,
    limit: int = 20,
    sort_by: str = Query("created_at", description="Field to sort by"),
    order: str = Query("desc", description="asc or desc"),
    profile_id: Optional[UUID] = None,
    title: Optional[str] = None,
    company_name: Optional[str] = None,
    employment_type: Optional[EmploymentType] = None,
    domain: Optional[List[Domain]] = Query(None),
    location: Optional[UUID] = None,
    location_type: Optional[WorkLocationType] = None,
    currently_working: Optional[bool] = None,
    start_date_after: Optional[str] = None,
    start_date_before: Optional[str] = None,
    session: Session = Depends(get_session),
):
    service = WorkExperienceService(session)
    logger.info(
        f"Listing Work Experiences: skip={skip}, limit={limit}, sort_by={sort_by}, order={order}, "
        f"profile_id={profile_id}, title={title}, company_name={company_name}, "
        f"employment_type={employment_type}, domain={domain}, location={location}, "
        f"location_type={location_type}, currently_working={currently_working}, "
        f"start_date_after={start_date_after}, start_date_before={start_date_before}"
    )
    work_experiences = service.list_work_experiences(
        skip,
        limit,
        sort_by,
        order,
        profile_id,
        title,
        company_name,
        employment_type,
        domain,
        location,
        location_type,
        currently_working,
        start_date_after,
        start_date_before,
    )
    logger.info(f"Returned {len(work_experiences)} work experiences")
    return work_experiences


@router.get("/autocomplete/", response_model=List[ReadWorkExperience])
def autocomplete_work_experiences(
    query: str,
    field: str = Query("title", description="Field to search against"),
    limit: int = 10,
    session: Session = Depends(get_session),
):
    service = WorkExperienceService(session)
    logger.info(f"Autocomplete query='{query}' field='{field}' limit={limit}")
    results = service.autocomplete_work_experiences(query, field, limit)
    logger.info(f"Autocomplete returned {len(results)} results")
    return results


@router.put("/{work_experience_id}", response_model=ReadWorkExperience)
def update_work_experience(
    work_experience_id: UUID, work_experience_update: UpdateWorkExperience, session: Session = Depends(get_session)
):
    service = WorkExperienceService(session)
    logger.info(
        f"Updating Work Experience ID: {work_experience_id} with data: {work_experience_update.dict(exclude_unset=True)}"
    )
    try:
        work_experience = service.update_work_experience(work_experience_id, work_experience_update)
        if not work_experience:
            logger.warning(f"Attempted update for missing Work Experience: {work_experience_id}")
            raise HTTPException(status_code=404, detail="Work Experience not found")
        logger.info(f"Updated Work Experience ID: {work_experience.id}")
        return work_experience
    except ValueError as e:
        logger.warning(f"Failed to update work experience: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error updating work experience: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{work_experience_id}", response_model=ReadWorkExperience)
def delete_work_experience(work_experience_id: UUID, session: Session = Depends(get_session)):
    service = WorkExperienceService(session)
    logger.info(f"Deleting Work Experience ID: {work_experience_id}")
    work_experience = service.delete_work_experience(work_experience_id)
    if not work_experience:
        logger.warning(f"Attempted delete for missing Work Experience: {work_experience_id}")
        raise HTTPException(status_code=404, detail="Work Experience not found")
    logger.info(f"Deleted Work Experience ID: {work_experience.id}")
    return work_experience