# Controllers/users_controller.py

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from uuid import UUID
from sqlmodel import Session

from Schema.user_schema import CreateUser, UpdateUser, ReadUser
from Services.User.user_service import UserService
from Settings.logging_config import setup_logging
from db import get_session

logger = setup_logging()

router = APIRouter(prefix="/Dijkstra/v1/u", tags=["Users"])


@router.post("/", response_model=ReadUser)
def create_user(user_create: CreateUser, session: Session = Depends(get_session)):
    service = UserService(session)
    logger.info(f"Creating User: {user_create.github_user_name}")
    try:
        user = service.create_user(user_create)
        logger.info(f"Created User with ID: {user.id}")
        return user
    except ValueError as e:
        logger.warning(f"Failed to create user: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{user_id}", response_model=ReadUser)
def get_user(user_id: UUID, session: Session = Depends(get_session)):
    service = UserService(session)
    logger.info(f"Fetching User with ID: {user_id}")
    user = service.get_user(user_id)
    if not user:
        logger.warning(f"User not found: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/github/{github_user_name}", response_model=ReadUser)
def get_user_by_github_username(github_user_name: str, session: Session = Depends(get_session)):
    service = UserService(session)
    logger.info(f"Fetching User with GitHub username: {github_user_name}")
    user = service.get_user_by_github_username(github_user_name)
    if not user:
        logger.warning(f"User not found with GitHub username: {github_user_name}")
        raise HTTPException(status_code=404, detail="User not found")
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
    logger.info(
        f"Updating User ID: {user_id} with data: {user_update.dict(exclude_unset=True)}"
    )
    try:
        user = service.update_user(user_id, user_update)
        if not user:
            logger.warning(f"Attempted update for missing User: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")
        logger.info(f"Updated User ID: {user.id}")
        return user
    except ValueError as e:
        logger.warning(f"Failed to update user: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error updating user: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{user_id}", response_model=ReadUser)
def delete_user(user_id: UUID, session: Session = Depends(get_session)):
    service = UserService(session)
    logger.info(f"Deleting User ID: {user_id}")
    user = service.delete_user(user_id)
    if not user:
        logger.warning(f"Attempted delete for missing User: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Deleted User ID: {user.id}")
    return user