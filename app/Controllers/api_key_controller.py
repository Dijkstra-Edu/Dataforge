from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from sqlmodel import Session

from Entities.UserDTOs.api_key_entity import CreateAPIKey, ReadAPIKey, UpdateAPIKey, APIKeyResponse
from Services.User.api_key_service import APIKeyService
from Security.jwt_dependencies import get_current_user, get_current_user_with_token, TokenPayload
from Schema.SQL.Models.models import User
from Settings.logging_config import setup_logging
from db import get_session

logger = setup_logging()

router = APIRouter(prefix="/Dijkstra/v1/api-keys", tags=["API Keys"])


def _ensure_owner(current_user: User, github_username: str) -> None:
    """Raise 403 if the authenticated user is not the owner of the resource.
    current_user is derived from the verified JWT (get_current_user loads User by
    token_payload.github_username), so this compares token identity to path param.
    """
    if current_user.github_user_name != github_username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access API keys for your own account",
        )


@router.post("/{github_username}", response_model=APIKeyResponse)
def create_api_key(
    github_username: str,
    create_data: CreateAPIKey,
    user_and_token: tuple[User, TokenPayload] = Depends(get_current_user_with_token),
    session: Session = Depends(get_session),
):
    """Create a new API key for the given GitHub username. Requires JWT; user must own the account."""
    current_user, token_payload = user_and_token
    _ensure_owner(current_user, github_username)
    service = APIKeyService(session)
    logger.info(f"Creating API key for user: {github_username}")
    user_roles = current_user.roles or []
    
    api_key_response = service.create_api_key(
        github_username=github_username,
        user_roles=user_roles,
        create_data=create_data,
    )
    
    logger.info(f"API key created successfully for user: {github_username}")
    return api_key_response


@router.get("/{github_username}", response_model=List[ReadAPIKey])
def list_api_keys(
    github_username: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """List all API keys for the given GitHub username. Requires JWT; user must own the account."""
    _ensure_owner(current_user, github_username)
    service = APIKeyService(session)
    logger.info(f"Listing API keys for user: {github_username}")
    
    api_keys = service.list_api_keys(github_username)
    logger.info(f"Found {len(api_keys)} API keys for user: {github_username}")
    return api_keys


@router.delete("/{api_key_id}", response_model=dict)
def revoke_api_key(
    api_key_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Revoke (deactivate) an API key. Requires JWT authentication."""
    service = APIKeyService(session)
    logger.info(f"Revoking API key {api_key_id} for user: {current_user.github_user_name}")
    
    result = service.revoke_api_key(api_key_id, current_user.github_user_name)
    logger.info(f"API key {api_key_id} revoked successfully")
    return result


@router.put("/{api_key_id}", response_model=ReadAPIKey)
def update_api_key(
    api_key_id: UUID,
    update_data: UpdateAPIKey,
    user_and_token: tuple[User, TokenPayload] = Depends(get_current_user_with_token),
    session: Session = Depends(get_session),
):
    """Update an API key. Requires JWT authentication."""
    current_user, token_payload = user_and_token
    service = APIKeyService(session)
    logger.info(f"Updating API key {api_key_id} for user: {current_user.github_user_name}")

    # Get user roles from database
    user_roles = current_user.roles or []
    
    updated_key = service.update_api_key(
        api_key_id=api_key_id,
        github_username=current_user.github_user_name,
        user_roles=user_roles,
        update_data=update_data,
    )
    
    logger.info(f"API key {api_key_id} updated successfully")
    return updated_key

