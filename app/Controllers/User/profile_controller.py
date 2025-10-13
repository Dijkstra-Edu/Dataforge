from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from uuid import UUID
from sqlmodel import Session

from Entities.UserDTOs.profile_entity import CreateProfile, UpdateProfile, ReadProfile
from Entities.UserDTOs.extended_entities import ReadProfileFull, ReadProfileWithUser

from Settings.logging_config import setup_logging
from Services.User.profile_service import ProfileService
from db import get_session

logger = setup_logging()

router = APIRouter(prefix="/Dijkstra/v1/profile", tags=["Profiles"])


@router.post("/", response_model=ReadProfile)
def create_profile(profile_create: CreateProfile, session: Session = Depends(get_session)):
    service = ProfileService(session)
    logger.info(f"Creating Profile for user ID: {profile_create.user_id}")
    profile = service.create_profile(profile_create)
    logger.info(f"Created Profile with ID: {profile.id}")
    return profile


@router.get("/id/{profile_id}")
def get_profile_by_id(
    profile_id: UUID,
    all_data: bool = Query(False, description="Include user details"),
    session: Session = Depends(get_session)
):
    """
    Get profile by ID.
    
    - If all_data=False: Returns basic profile data only
    - If all_data=True: Returns profile with user details
    """
    service = ProfileService(session)
    logger.info(f"Fetching Profile with ID: {profile_id}, all_data={all_data}")
    
    if all_data:
        profile = service.get_profile_with_user_details(profile_id)
        return profile
    else:
        profile = service.get_profile(profile_id)
        return profile


@router.get("/{github_username}")
def get_profile_by_github_username(
    github_username: str,
    all_data: bool = Query(False, description="Include all nested data (education, work experience, certifications, etc.)"),
    session: Session = Depends(get_session)
):
    """
    Get profile by GitHub username.
    
    - If all_data=False: Returns basic profile data only
    - If all_data=True: Returns full profile with all nested relationships
    """
    service = ProfileService(session)
    logger.info(f"Fetching Profile for GitHub username: {github_username}, all_data={all_data}")
    
    if all_data:
        profile = service.get_profile_full_data_by_github_username(github_username)
        return profile
    else:
        from Services.User.user_service import UserService
        user_service = UserService(session)
        user_id = user_service.get_user_id_by_github_username(github_username)
        profile = service.get_profile_by_user_id(user_id)
        return profile


@router.get("/user/{user_id}", response_model=ReadProfileWithUser)
def get_profile_by_user_id(user_id: UUID, session: Session = Depends(get_session)):
    service = ProfileService(session)
    logger.info(f"Fetching Profile for user ID: {user_id}")
    profile = service.get_profile_by_user_id(user_id)
    return profile


@router.get("/", response_model=List[ReadProfile])
def list_profiles(
    skip: int = 0,
    limit: int = 20,
    sort_by: str = Query("created_at", description="Field to sort by"),
    order: str = Query("desc", description="asc or desc"),
    user_id: Optional[UUID] = None,
    session: Session = Depends(get_session),
):
    service = ProfileService(session)
    logger.info(
        f"Listing Profiles: skip={skip}, limit={limit}, sort_by={sort_by}, order={order}, "
        f"user_id={user_id}"
    )
    profiles = service.list_profiles(
        skip,
        limit,
        sort_by,
        order,
        user_id,
    )
    logger.info(f"Returned {len(profiles)} profiles")
    return profiles


@router.put("/{profile_id}", response_model=ReadProfile)
def update_profile(
    profile_id: UUID, profile_update: UpdateProfile, session: Session = Depends(get_session)
):
    service = ProfileService(session)
    logger.info(f"Updating Profile ID: {profile_id} with data: {profile_update.dict(exclude_unset=True)}")
    profile = service.update_profile(profile_id, profile_update)
    logger.info(f"Updated Profile ID: {profile.id}")
    return profile


@router.delete("/{profile_id}", response_model=ReadProfile)
def delete_profile(profile_id: UUID, session: Session = Depends(get_session)):
    service = ProfileService(session)
    logger.info(f"Deleting Profile ID: {profile_id}")
    message = service.delete_profile(profile_id)
    logger.info(message)
    return {"detail": message}