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
@router.get("/id/{link_id}", response_model=ReadLinks)
def get_links(
    link_id: UUID,
    session: Session = Depends(get_session),
):
    service = LinksService(session)
    logger.info(f"Fetching Links with ID: {link_id}")
    links = service.get_links(link_id)
    return links


# Get by GitHub username
@router.get("/{github_username}", response_model=ReadLinks)
def get_links_by_github_username(
    github_username: str,
    session: Session = Depends(get_session),
):
    service = LinksService(session)
    logger.info(f"Fetching Links for GitHub username: {github_username}")
    links = service.get_links_by_github_username(github_username)
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
    primary_email: Optional[str] = None,
    secondary_email: Optional[str] = None,
    school_email: Optional[str] = None,
    work_email: Optional[str] = None,
    session: Session = Depends(get_session),
):
    service = LinksService(session)
    logger.info(
        f"Listing Links: skip={skip}, limit={limit}, sort_by={sort_by}, order={order}, "
        f"github_user_name={github_user_name}, linkedin_user_name={linkedin_user_name}, "
        f"leetcode_user_name={leetcode_user_name}, orcid_id={orcid_id}, "
        f"primary_email={primary_email}, secondary_email={secondary_email}, "
        f"school_email={school_email}, work_email={work_email}"
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
        primary_email=primary_email,
        secondary_email=secondary_email,
        school_email=school_email,
        work_email=work_email,
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
