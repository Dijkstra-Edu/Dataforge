from typing import List
from fastapi import APIRouter, Depends, Query
from uuid import UUID
from sqlmodel import Session

from Settings.logging_config import setup_logging
from Entities.UserDTOs.volunteering_entity import CreateVolunteering, ReadVolunteering, ReadVolunteeringWithRelations, UpdateVolunteering
from Services.User.volunteering_service import VolunteeringService
from db import get_session

logger = setup_logging()

router = APIRouter(prefix="/Dijkstra/v1/volunteering", tags=["Volunteering"])


@router.post("/", response_model=ReadVolunteering)
def create_volunteering(volunteering_create: CreateVolunteering, session: Session = Depends(get_session)):
    service = VolunteeringService(session)
    logger.info(f"Creating volunteering at {volunteering_create.organization} for role {volunteering_create.role}")
    volunteering = service.create_volunteering(volunteering_create)
    logger.info(f"Created volunteering with ID: {volunteering.id}")
    return volunteering


@router.get("/id/{volunteering_id}", response_model=ReadVolunteeringWithRelations)
def get_volunteering(volunteering_id: UUID, session: Session = Depends(get_session)):
    service = VolunteeringService(session)
    logger.info(f"Fetching volunteering with ID: {volunteering_id}")
    volunteering = service.get_volunteering(volunteering_id)
    logger.info(f"Fetched volunteering with ID: {volunteering.id}")
    return volunteering


@router.get("/{github_username}", response_model=List[ReadVolunteering])
def get_volunteering_by_github_username(github_username: str, session: Session = Depends(get_session)):
    service = VolunteeringService(session)
    logger.info(f"Fetching Volunteering entries for GitHub username: {github_username}")
    volunteering = service.get_volunteering_by_github_username(github_username)
    return volunteering


@router.get("/profile/{profile_id}", response_model=List[ReadVolunteering])
def get_volunteering_by_profile_id(profile_id: UUID, session: Session = Depends(get_session)):
    service = VolunteeringService(session)
    logger.info(f"Fetching volunteering entries for profile ID: {profile_id}")
    volunteering_entries = service.get_volunteering_by_profile_id(profile_id)
    logger.info(f"Returned {len(volunteering_entries)} volunteering entries for profile {profile_id}")
    return volunteering_entries


@router.get("/", response_model=List[ReadVolunteering])
def list_volunteering(
    skip: int = 0,
    limit: int = 20,
    session: Session = Depends(get_session),
):
    service = VolunteeringService(session)
    logger.info(f"Listing volunteering entries: skip={skip}, limit={limit}")
    volunteering_entries = service.list_volunteering(skip=skip, limit=limit)
    logger.info(f"Returned {len(volunteering_entries)} volunteering entries")
    return volunteering_entries


@router.put("/{volunteering_id}", response_model=ReadVolunteering)
def update_volunteering(volunteering_id: UUID, volunteering_update: UpdateVolunteering, session: Session = Depends(get_session)):
    service = VolunteeringService(session)
    logger.info(f"Updating volunteering ID: {volunteering_id} with data: {volunteering_update.dict(exclude_unset=True)}")
    volunteering = service.update_volunteering(volunteering_id, volunteering_update)
    logger.info(f"Updated volunteering ID: {volunteering.id}")
    return volunteering


@router.delete("/{volunteering_id}")
def delete_volunteering(volunteering_id: UUID, session: Session = Depends(get_session)):
    service = VolunteeringService(session)
    logger.info(f"Deleting volunteering ID: {volunteering_id}")
    message = service.delete_volunteering(volunteering_id)
    logger.info(f"Deleted volunteering ID: {volunteering_id}")
    return {"detail": message}
