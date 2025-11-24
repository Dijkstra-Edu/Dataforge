# Controllers/users_controller.py

from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from uuid import UUID
from sqlmodel import Session

from Entities.UserDTOs.user_entity import CreateUser, ReadUserAuthDetails, UpdateUser, ReadUser, OnboardUser, OnboardCheckResponse, ReadUserCardDetails, ReadUserPersonalDetails, UpdateUserPersonalDetails
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
    session: Session = Depends(get_session)
):
    """
    Check if a user has completed onboarding by GitHub username.
    """    
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

# TODO: Create an update endpoint for completing onboarding


@router.get("/id/{user_id}")
def get_user_by_id(
    user_id: UUID,
    all_data: bool = Query(False, description="Include all related data (links, profile with nested entities)"),
    session: Session = Depends(get_session)
):
    """
    Get user by ID.
    
    - If all_data=False: Returns basic user data only
    - If all_data=True: Returns user with links and full profile including all nested entities
    """
    service = UserService(session)
    logger.info(f"Fetching User with ID: {user_id}, all_data={all_data}")
    
    if all_data:
        user_data = service.get_user_data_by_user_id(user_id, full_data=True)
        return user_data
    else:
        user = service.get_user(user_id)
        return user


@router.get("/{github_username}")
def get_user_by_github_username(
    github_username: str,
    all_data: bool = Query(False, description="Include all related data (links, profile with nested entities)"),
    session: Session = Depends(get_session)
):
    """
    Get user by GitHub username.
    
    - If all_data=False: Returns basic user data only
    - If all_data=True: Returns user with links and full profile including:
      - Education (with locations)
      - Work Experience (with locations)
      - Certifications
      - Publications
      - Volunteering
      - Projects
      - Leetcode (excluded for now, returns None)
    """
    service = UserService(session)
    logger.info(f"Fetching User with GitHub username: {github_username}, all_data={all_data}")
    
    if all_data:
        user_data = service.get_user_data_by_github_username(github_username, full_data=True)
        return user_data
    else:
        user = service.get_user_by_github_username(github_username)
        return user

@router.get("/card/{github_username}", response_model=ReadUserCardDetails)
def get_user_card_details_by_github_username(
    github_username: str,
    session: Session = Depends(get_session)
):
    """
    Get user card details by GitHub username.
    """
    service = UserService(session)
    logger.info(f"Fetching User card details with GitHub username: {github_username}")
    user_data = service.get_user_card_details_by_github_username(github_username)
    logger.info(f"User card details fetched successfully for GitHub username: {github_username}")
    return user_data

@router.get("/personal-details/{github_username}", response_model=ReadUserPersonalDetails)
def get_personal_details_by_github_username(
    github_username: str,
    session: Session = Depends(get_session)
):
    """
    Get user personal details by GitHub username.
    """
    service = UserService(session)
    logger.info(f"Fetching User personal details with GitHub username: {github_username}")
    user_data = service.get_user_personal_details_by_github_username(github_username)
    logger.info(f"User personal details fetched successfully for GitHub username: {github_username}")
    return user_data

@router.get("/auth/{github_username}", response_model=ReadUserAuthDetails)
def get_user_auth_details_by_github_username(
    github_username: str,
    session: Session = Depends(get_session)
):
    """
    Get user auth details by GitHub username.
    """
    service = UserService(session)
    logger.info(f"Fetching User auth details with GitHub username: {github_username}")
    user_data = service.get_user_auth_details_by_github_username(github_username)
    logger.info(f"User auth details fetched successfully for GitHub username: {github_username}")
    return user_data

@router.put("/personal-details/{github_username}", response_model=ReadUserPersonalDetails)
def update_user_personal_details_by_github_username(
    github_username: str,
    user_personal_details_update: UpdateUserPersonalDetails,
    session: Session = Depends(get_session)
):
    """
    Update user personal details by GitHub username.
    Updates both User and Links tables with the provided personal details.
    """
    service = UserService(session)
    logger.info(f"Updating User personal details with GitHub username: {github_username}")
    user_data = service.update_user_personal_details_by_github_username(github_username, user_personal_details_update)
    logger.info(f"User personal details updated successfully for GitHub username: {github_username}")
    return user_data

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


@router.put("/id/{user_id}", response_model=ReadUser)
def update_user_by_id(
    user_id: UUID, user_update: UpdateUser, session: Session = Depends(get_session)
):
    service = UserService(session)
    logger.info(f"Updating User ID: {user_id} with data: {user_update.dict(exclude_unset=True)}")
    user = service.update_user(user_id, user_update)
    logger.info(f"Updated User ID: {user.id}")
    return user


@router.put("/{github_username}", response_model=ReadUser)
def update_user_by_github_username(
    github_username: str, user_update: UpdateUser, session: Session = Depends(get_session)
):
    service = UserService(session)
    logger.info(f"Updating User with GitHub username: {github_username} with data: {user_update.dict(exclude_unset=True)}")
    user = service.update_user_by_github_username(github_username, user_update)
    logger.info(f"Updated User ID: {user.id}")
    return user


@router.delete("/id/{user_id}", response_model=dict)
def delete_user_by_id(user_id: UUID, session: Session = Depends(get_session)):
    service = UserService(session)
    logger.info(f"Deleting User ID: {user_id}")
    message = service.delete_user(user_id)
    logger.info(message)
    return {"detail": message}


@router.delete("/{github_username}", response_model=dict)
def delete_user_by_github_username(github_username: str, session: Session = Depends(get_session)):
    service = UserService(session)
    logger.info(f"Deleting User with GitHub username: {github_username}")
    message = service.delete_user_by_github_username(github_username)
    logger.info(message)
    return {"detail": message}