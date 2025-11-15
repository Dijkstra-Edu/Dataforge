from datetime import datetime, timezone
from typing import Optional
import hashlib

from fastapi import Depends, Header, HTTPException, status
from sqlmodel import Session

from Schema.SQL.Models.models import APIKey
from Repository.User.api_key_repository import APIKeyRepository
from Security.jwt_dependencies import _decode_authorization_header
from db import get_session


def _hash_key(key: str) -> str:
    """Hash API key with SHA256."""
    return hashlib.sha256(key.encode()).hexdigest()


def verify_api_key(
    authorization: Optional[str] = Header(default=None),
    session: Session = Depends(get_session),
) -> APIKey:
    """Verify API key from Authorization header."""
    token = _decode_authorization_header(authorization)
    
    # Hash the token and look up by key_hash
    key_hash = _hash_key(token)
    repo = APIKeyRepository(session)
    api_key = repo.get_active_by_key_hash(key_hash)
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or inactive API key",
        )
    
    # Check expiration
    if api_key.expires_in and api_key.expires_in < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key has expired",
        )
    
    # Check active status
    if not api_key.active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is inactive",
        )
    
    return api_key


def auth_api_key_required(
    api_key: APIKey = Depends(verify_api_key),
) -> APIKey:
    """API key-only authentication dependency."""
    return api_key

