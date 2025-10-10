# Controllers/users_controller.py

from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from uuid import UUID
from sqlmodel import Session

from Entities.UserDTOs.user_entity import CreateUser, UpdateUser, ReadUser, OnboardUser, OnboardCheckResponse
from Services.User.user_service import UserService
from Settings.logging_config import setup_logging
from db import get_session

logger = setup_logging()

router = APIRouter(prefix="/Dijkstra/v1/u", tags=["Users"])


@router.post("/", response_model=ReadUser)
def create_user(user_create: CreateUser, session: Session = Depends(get_session)):
    service = UserService(session)
    logger.info(f"Creating User: {user_create.github_user_name}")
    user = service.create_user(user_create)
    logger.info(f"Created User with ID: {user.id}")
    return user


@router.get("/onboard", response_model=OnboardCheckResponse)
def check_onboarding(
    username: str = Query(..., description="GitHub username to check"),
    check: bool = Query(False, description="Check onboarding status"),
    session: Session = Depends(get_session)
):
    """
    Check if a user has completed onboarding by GitHub username.
    Use ?check=true to activate this endpoint.
    """
    if not check:
        logger.warning("Onboard check endpoint called without check=true parameter")
        return OnboardCheckResponse(onboarded=False, user_id=None)
    
    service = UserService(session)
    logger.info(f"Checking onboarding status for GitHub username: {username}")
    result = service.check_onboarding_status(username)
    logger.info(f"Onboarding status for {username}: onboarded={result.onboarded}, user_id={result.user_id}")
    return result


@router.post("/onboard", response_model=ReadUser)
def onboard_user(onboard_data: OnboardUser, session: Session = Depends(get_session)):
    """
    Onboard a new user - creates User with Profile and Links, and marks onboarding as complete.
    """
    service = UserService(session)
    logger.info(f"Onboarding User: {onboard_data.github_user_name}")
    user = service.onboard_user(onboard_data)
    logger.info(f"Successfully onboarded User with ID: {user.id}")
    return user


@router.get("/{user_id}", response_model=ReadUser)
def get_user(user_id: UUID, session: Session = Depends(get_session)):
    service = UserService(session)
    logger.info(f"Fetching User with ID: {user_id}")
    user = service.get_user(user_id)
    return user


@router.get("/github/{github_user_name}", response_model=ReadUser)
def get_user_by_github_username(github_user_name: str, session: Session = Depends(get_session)):
    service = UserService(session)
    logger.info(f"Fetching User with GitHub username: {github_user_name}")
    user = service.get_user_by_github_username(github_user_name)
    return user


@router.get("/", response_model=List[ReadUser])
def list_users(
    skip: int = 0,
    limit: int = 20,
    sort_by: str = Query("created_at", description="Field to sort by"),
    order: str = Query("desc", description="asc or desc"),
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    github_user_name: Optional[str] = None,
    rank: Optional[str] = None,
    min_streak: Optional[int] = Query(None, ge=0),
    max_streak: Optional[int] = Query(None, ge=0),
    session: Session = Depends(get_session),
):
    service = UserService(session)
    logger.info(
        f"Listing Users: skip={skip}, limit={limit}, sort_by={sort_by}, order={order}, "
        f"first_name={first_name}, last_name={last_name}, github_user_name={github_user_name}, "
        f"rank={rank}, min_streak={min_streak}, max_streak={max_streak}"
    )
    users = service.list_users(
        skip,
        limit,
        sort_by,
        order,
        first_name,
        last_name,
        github_user_name,
        rank,
        min_streak,
        max_streak,
    )
    logger.info(f"Returned {len(users)} users")
    return users


@router.get("/autocomplete/", response_model=List[ReadUser])
def autocomplete_users(
    query: str,
    field: str = Query("github_user_name", description="Field to search against"),
    limit: int = 10,
    session: Session = Depends(get_session),
):
    service = UserService(session)
    logger.info(f"Autocomplete query='{query}' field='{field}' limit={limit}")
    results = service.autocomplete_users(query, field, limit)
    logger.info(f"Autocomplete returned {len(results)} results")
    return results


@router.put("/{user_id}", response_model=ReadUser)
def update_user(
    user_id: UUID, user_update: UpdateUser, session: Session = Depends(get_session)
):
    service = UserService(session)
    logger.info(f"Updating User ID: {user_id} with data: {user_update.dict(exclude_unset=True)}")
    user = service.update_user(user_id, user_update)
    logger.info(f"Updated User ID: {user.id}")
    return user


@router.delete("/{user_id}", response_model=ReadUser)
def delete_user(user_id: UUID, session: Session = Depends(get_session)):
    service = UserService(session)
    logger.info(f"Deleting User ID: {user_id}")
    message = service.delete_user(user_id)
    logger.info(message)
    return {"detail": message}