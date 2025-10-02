from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from uuid import UUID
from sqlmodel import Session

from Settings.logging_config import setup_logging
from Entities.UserDTOs.links_entity import CreateLinks, ReadLinks, UpdateLinks
from Services.User.links_service import LinksService
from db import get_session

logger = setup_logging()

router = APIRouter(prefix="/Dijkstra/v1/links", tags=["Links"])

# Create
@router.post("/", response_model=ReadLinks)
def create_links(
    links_create: CreateLinks,
    session: Session = Depends(get_session),
):
    service = LinksService(session)
    logger.info(f"Creating links for user ID: {links_create.user_id}")
    links = service.create_links(links_create)
    logger.info(f"Created Links with ID: {links.id}")
    return links

# Get by ID
@router.get("/{link_id}", response_model=ReadLinks)
def get_links(
    link_id: UUID,
    session: Session = Depends(get_session),
):
    service = LinksService(session)
    logger.info(f"Fetching Links with ID: {link_id}")
    links = service.get_links(link_id)
    return links

# Get by User ID
@router.get("/user/{user_id}", response_model=ReadLinks)
def get_links_by_user(
    user_id: UUID,
    session: Session = Depends(get_session),
):
    service = LinksService(session)
    logger.info(f"Fetching Links for User ID: {user_id}")
    links = service.get_links_by_user_id(user_id)
    return links

# List with pagination, filtering, sorting
@router.get("/", response_model=List[ReadLinks])
def list_links(
    skip: int = 0,
    limit: int = 20,
    sort_by: str = Query("created_at", description="Field to sort by"),
    order: str = Query("desc", description="asc or desc"),
    github_user_name: Optional[str] = None,
    linkedin_user_name: Optional[str] = None,
    leetcode_user_name: Optional[str] = None,
    orcid_id: Optional[str] = None,
    session: Session = Depends(get_session),
):
    service = LinksService(session)
    logger.info(
        f"Listing Links: skip={skip}, limit={limit}, sort_by={sort_by}, order={order}, "
        f"github_user_name={github_user_name}, linkedin_user_name={linkedin_user_name}, "
        f"leetcode_user_name={leetcode_user_name}, orcid_id={orcid_id}"
    )
    links = service.list_links(
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        order=order,
        github_user_name=github_user_name,
        linkedin_user_name=linkedin_user_name,
        leetcode_user_name=leetcode_user_name,
        orcid_id=orcid_id,
    )
    logger.info(f"Returned {len(links)} links")
    return links

# Update
@router.put("/{link_id}", response_model=ReadLinks)
def update_links(
    link_id: UUID,
    links_update: UpdateLinks,
    session: Session = Depends(get_session),
):
    service = LinksService(session)
    logger.info(f"Updating Links ID: {link_id} with data: {links_update.dict(exclude_unset=True)}")
    links = service.update_links(link_id, links_update)
    logger.info(f"Updated Links ID: {links.id}")
    return links

# Delete
@router.delete("/{link_id}")
def delete_links(
    link_id: UUID,
    session: Session = Depends(get_session),
):
    service = LinksService(session)
    logger.info(f"Deleting Links ID: {link_id}")
    message = service.delete_links(link_id)
    logger.info(message)
    return {"detail": message}
