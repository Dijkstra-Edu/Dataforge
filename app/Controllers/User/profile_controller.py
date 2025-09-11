from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from uuid import UUID
from sqlmodel import Session

from Entities.UserDTOs.profile_entity import CreateProfile, UpdateProfile, ReadProfile, ReadProfileWithUser

from Settings.logging_config import setup_logging
from Services.User.profile_service import ProfileService
from db import get_session

logger = setup_logging()

router = APIRouter(prefix="/Dijkstra/v1/profile", tags=["Profiles"])


@router.post("/", response_model=ReadProfile)
def create_profile(profile_create: CreateProfile, session: Session = Depends(get_session)):
    service = ProfileService(session)
    logger.info(f"Creating Profile for user ID: {profile_create.user_id}")
    try:
        profile = service.create_profile(profile_create)
        logger.info(f"Created Profile with ID: {profile.id}")
        return profile
    except ValueError as e:
        logger.warning(f"Failed to create profile: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error creating profile: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{profile_id}", response_model=ReadProfileWithUser)
def get_profile(profile_id: UUID, session: Session = Depends(get_session)):
    service = ProfileService(session)
    logger.info(f"Fetching Profile with ID: {profile_id}")
    profile = service.get_profile(profile_id)
    if not profile:
        logger.warning(f"Profile not found: {profile_id}")
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.get("/user/{user_id}", response_model=ReadProfileWithUser)
def get_profile_by_user_id(user_id: UUID, session: Session = Depends(get_session)):
    service = ProfileService(session)
    logger.info(f"Fetching Profile for user ID: {user_id}")
    profile = service.get_profile_by_user_id(user_id)
    if not profile:
        logger.warning(f"Profile not found for user ID: {user_id}")
        raise HTTPException(status_code=404, detail="Profile not found")
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
    logger.info(
        f"Updating Profile ID: {profile_id} with data: {profile_update.dict(exclude_unset=True)}"
    )
    try:
        profile = service.update_profile(profile_id, profile_update)
        if not profile:
            logger.warning(f"Attempted update for missing Profile: {profile_id}")
            raise HTTPException(status_code=404, detail="Profile not found")
        logger.info(f"Updated Profile ID: {profile.id}")
        return profile
    except ValueError as e:
        logger.warning(f"Failed to update profile: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error updating profile: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{profile_id}", response_model=ReadProfile)
def delete_profile(profile_id: UUID, session: Session = Depends(get_session)):
    service = ProfileService(session)
    logger.info(f"Deleting Profile ID: {profile_id}")
    profile = service.delete_profile(profile_id)
    if not profile:
        logger.warning(f"Attempted delete for missing Profile: {profile_id}")
        raise HTTPException(status_code=404, detail="Profile not found")
    logger.info(f"Deleted Profile ID: {profile.id}")
    return profile