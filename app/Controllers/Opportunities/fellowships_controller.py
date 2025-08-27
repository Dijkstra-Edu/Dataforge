from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
import logging

from Schema.fellowships_schema import CreateFellowship, UpdateFellowship, ReadFellowship
from Services.Opportunities.fellowships_service import FellowshipService
from db import get_session
from Settings.logging_config import setup_logging

logger = setup_logging()

router = APIRouter(prefix="/Dijkstra/v1/fellowships", tags=["Fellowships"])


@router.post("/", response_model=ReadFellowship)
def create_fellowship(fellowship_create: CreateFellowship, session: Session = Depends(get_session)):
    service = FellowshipService(session)
    logger.info(f"Creating Fellowship: {fellowship_create.title}")
    fellowship = service.create_fellowship(fellowship_create)
    logger.info(f"Fellowship created with ID: {fellowship.id}")
    return fellowship


@router.get("/{fellowship_id}", response_model=ReadFellowship)
def get_fellowship(fellowship_id: UUID, session: Session = Depends(get_session)):
    service = FellowshipService(session)
    logger.info(f"Fetching Fellowship with ID: {fellowship_id}")
    fellowship = service.get_fellowship(fellowship_id)
    if not fellowship:
        logger.warning(f"Fellowship not found: {fellowship_id}")
        raise HTTPException(status_code=404, detail="Fellowship not found")
    return fellowship


@router.get("/", response_model=List[ReadFellowship])
def list_fellowships(
    skip: int = 0,
    limit: int = 20,
    sort_by: str = "created_at",
    order: str = "desc",
    title: Optional[str] = None,
    organization: Optional[UUID] = None,
    location: Optional[str] = None,
    featured: Optional[bool] = None,
    session: Session = Depends(get_session),
):
    service = FellowshipService(session)
    logger.info(f"Listing Fellowships: skip={skip}, limit={limit}, sort_by={sort_by}, order={order}")
    fellowships = service.list_fellowships(skip, limit, sort_by, order, title, organization, location, featured)
    logger.info(f"Returned {len(fellowships)} Fellowships")
    return fellowships


@router.put("/{fellowship_id}", response_model=ReadFellowship)
def update_fellowship(fellowship_id: UUID, fellowship_update: UpdateFellowship, session: Session = Depends(get_session)):
    service = FellowshipService(session)
    logger.info(f"Updating Fellowship ID: {fellowship_id} with data: {fellowship_update.dict(exclude_unset=True)}")
    fellowship = service.update_fellowship(fellowship_id, fellowship_update)
    if not fellowship:
        logger.warning(f"Fellowship not found for update: {fellowship_id}")
        raise HTTPException(status_code=404, detail="Fellowship not found")
    logger.info(f"Fellowship updated: {fellowship.id}")
    return fellowship


@router.delete("/{fellowship_id}", response_model=ReadFellowship)
def delete_fellowship(fellowship_id: UUID, session: Session = Depends(get_session)):
    service = FellowshipService(session)
    logger.info(f"Deleting Fellowship ID: {fellowship_id}")
    fellowship = service.delete_fellowship(fellowship_id)
    if not fellowship:
        logger.warning(f"Fellowship not found for deletion: {fellowship_id}")
        raise HTTPException(status_code=404, detail="Fellowship not found")
    logger.info(f"Fellowship deleted: {fellowship.id}")
    return fellowship


@router.get("/autocomplete/", response_model=List[ReadFellowship])
def autocomplete_fellowships(query: str, field: str = "title", limit: int = 10, session: Session = Depends(get_session)):
    service = FellowshipService(session)
    logger.info(f"Autocomplete query='{query}' field='{field}' limit={limit}")
    results = service.autocomplete_fellowships(query, field, limit)
    logger.info(f"Autocomplete returned {len(results)} results")
    return results
