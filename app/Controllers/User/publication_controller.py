from typing import List
from fastapi import APIRouter, Depends
from uuid import UUID
from sqlmodel import Session

from Settings.logging_config import setup_logging
from Entities.UserDTOs.publication_entity import (
    CreatePublication,
    ReadPublication,
    ReadPublicationWithRelations,
    UpdatePublication,
)
from Services.User.publication_service import PublicationService
from db import get_session

logger = setup_logging()

router = APIRouter(prefix="/Dijkstra/v1/publications", tags=["Publications"])


@router.post("/", response_model=ReadPublication)
def create_publication(publication_create: CreatePublication, session: Session = Depends(get_session)):
    service = PublicationService(session)
    logger.info(f"Creating publication: {publication_create.title} by {publication_create.publisher}")
    publication = service.create_publication(publication_create)
    logger.info(f"Created publication with ID: {publication.id}")
    return publication


@router.get("/{publication_id}", response_model=ReadPublicationWithRelations)
def get_publication(publication_id: UUID, session: Session = Depends(get_session)):
    service = PublicationService(session)
    logger.info(f"Fetching publication with ID: {publication_id}")
    publication = service.get_publication(publication_id)
    logger.info(f"Fetched publication with ID: {publication.id}")
    return publication


@router.get("/profile/{profile_id}", response_model=List[ReadPublication])
def get_publications_by_profile_id(profile_id: UUID, session: Session = Depends(get_session)):
    service = PublicationService(session)
    logger.info(f"Fetching publications for profile ID: {profile_id}")
    publications = service.get_publications_by_profile_id(profile_id)
    logger.info(f"Returned {len(publications)} publications for profile {profile_id}")
    return publications


@router.get("/", response_model=List[ReadPublication])
def list_publications(
    skip: int = 0,
    limit: int = 20,
    session: Session = Depends(get_session),
):
    service = PublicationService(session)
    logger.info(f"Listing publications: skip={skip}, limit={limit}")
    publications = service.list_publications(skip=skip, limit=limit)
    logger.info(f"Returned {len(publications)} publications")
    return publications


@router.put("/{publication_id}", response_model=ReadPublication)
def update_publication(publication_id: UUID, publication_update: UpdatePublication, session: Session = Depends(get_session)):
    service = PublicationService(session)
    logger.info(f"Updating publication ID: {publication_id} with data: {publication_update.dict(exclude_unset=True)}")
    publication = service.update_publication(publication_id, publication_update)
    logger.info(f"Updated publication ID: {publication.id}")
    return publication


@router.delete("/{publication_id}")
def delete_publication(publication_id: UUID, session: Session = Depends(get_session)):
    service = PublicationService(session)
    logger.info(f"Deleting publication ID: {publication_id}")
    message = service.delete_publication(publication_id)
    logger.info(f"Deleted publication ID: {publication_id}")
    return {"detail": message}
