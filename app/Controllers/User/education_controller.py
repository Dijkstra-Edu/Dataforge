from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from uuid import UUID
from sqlmodel import Session

from Entities.UserDTOs.education_entity import CreateEducation, UpdateEducation, ReadEducation
from Services.User.education_service import EducationService
from Settings.logging_config import setup_logging
from db import get_session

logger = setup_logging()

router = APIRouter(prefix="/Dijkstra/v1/education", tags=["Education"])


@router.post("/", response_model=ReadEducation)
def create_education(education_create: CreateEducation, session: Session = Depends(get_session)):
    service = EducationService(session)
    logger.info(f"Creating Education entry for profile_id={education_create.profile_id}")
    education = service.create_education(education_create)
    logger.info(f"Created Education with ID: {education.id}")
    return education


@router.get("/{education_id}", response_model=ReadEducation)
def get_education(education_id: UUID, session: Session = Depends(get_session)):
    service = EducationService(session)
    logger.info(f"Fetching Education with ID: {education_id}")
    education = service.get_education(education_id)
    return education


@router.get("/", response_model=List[ReadEducation])
def list_educations(
    skip: int = 0,
    limit: int = 20,
    profile_id: Optional[UUID] = Query(None, description="Filter by Profile ID"),
    session: Session = Depends(get_session),
):
    service = EducationService(session)
    logger.info(f"Listing Education entries: skip={skip}, limit={limit}, profile_id={profile_id}")
    educations = service.list_educations(skip=skip, limit=limit, profile_id=profile_id)
    logger.info(f"Returned {len(educations)} education entries")
    return educations


@router.put("/{education_id}", response_model=ReadEducation)
def update_education(education_id: UUID, education_update: UpdateEducation, session: Session = Depends(get_session)):
    service = EducationService(session)
    logger.info(f"Updating Education ID: {education_id} with data: {education_update.dict(exclude_unset=True)}")
    education = service.update_education(education_id, education_update)
    logger.info(f"Updated Education ID: {education.id}")
    return education


@router.delete("/{education_id}")
def delete_education(education_id: UUID, session: Session = Depends(get_session)):
    service = EducationService(session)
    logger.info(f"Deleting Education ID: {education_id}")
    message = service.delete_education(education_id)
    logger.info(message)
    return {"detail": message}

@router.get("/profile/{profile_id}", response_model=List[ReadEducation])
def get_educations_by_profile(profile_id: UUID, session: Session = Depends(get_session)):
    service = EducationService(session)
    logger.info(f"Fetching Education entries for profile_id={profile_id}")
    educations = service.get_educations_by_profile(profile_id)
    logger.info(f"Returned {len(educations)} education entries for profile_id={profile_id}")
    return educations
