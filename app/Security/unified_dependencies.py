import os
from typing import Callable, Optional, Tuple
from fastapi import Depends, Header, HTTPException, status
from jose import JWTError
from pydantic import ValidationError
from sqlmodel import Session, select

from Schema.SQL.Enums.enums import Role
from Schema.SQL.Models.models import User
from Security.jwt_dependencies import (
    get_current_user,
    TokenPayload,
    _decode_authorization_header,
    _verify_jwt_token,
    PRIVILEGED_ROLES,
)
from Security.api_key_dependencies import verify_api_key
from Security.jwt_config import JWTSettings, get_jwt_settings
from Utils.error_codes import ErrorCodes
from Utils.errors import raise_api_error
from db import get_session


def auth_user_or_api_key(
    authorization: Optional[str] = Header(default=None),
    session: Session = Depends(get_session),
    settings: JWTSettings = Depends(get_jwt_settings),
) -> dict:
    """Unified authentication that tries JWT first, then API key."""
    user = None
    api_key = None
    is_dev = False
    identity = None
    mode = None
    
    # Try JWT first
    try:
        token = _decode_authorization_header(authorization)
        token_payload = _verify_jwt_token(token, settings)
        user = get_current_user(token_payload, session)
        is_dev = token_payload.is_dev or False
        identity = user.github_user_name
        mode = "jwt"
    except (HTTPException, JWTError, ValidationError):
        # JWT failed, try API key
        try:
            api_key = verify_api_key(authorization, session)
            identity = api_key.github_username
            # For API key, is_dev is False (no JWT token available)
            is_dev = False
            mode = "api_key"
        except HTTPException:
            # Both failed
            raise_api_error(
                code=ErrorCodes.AUTH_ERROR,
                error=ErrorCodes.AUTH_ERROR_A01,
                detail="Invalid authentication",
                status=status.HTTP_401_UNAUTHORIZED,
            )
    
    return {
        "mode": mode,
        "identity": identity,
        "user": user,
        "api_key": api_key,
        "is_dev": is_dev,
    }


def get_authenticated_user(
    auth_result: dict = Depends(auth_user_or_api_key),
    session: Session = Depends(get_session),
) -> User:
    """Get User object from either JWT or API key authentication."""
    if auth_result["mode"] == "jwt":
        return auth_result["user"]
    elif auth_result["mode"] == "api_key":
        # Look up user by github_username from API key
        api_key = auth_result["api_key"]
        statement = select(User).where(User.github_user_name == api_key.github_username)
        user = session.exec(statement).first()
        if not user:
            raise_api_error(
                code=ErrorCodes.AUTH_ERROR,
                error=ErrorCodes.AUTH_ERROR_A01,
                detail="User associated with API key not found",
                status=status.HTTP_401_UNAUTHORIZED,
            )
        user.roles = user.roles or []
        return user
    else:
        raise_api_error(
            code=ErrorCodes.AUTH_ERROR,
            error=ErrorCodes.AUTH_ERROR_A01,
            detail="Invalid authentication",
            status=status.HTTP_401_UNAUTHORIZED,
        )


def get_authenticated_user_with_token(
    auth_result: dict = Depends(auth_user_or_api_key),
    session: Session = Depends(get_session),
    authorization: Optional[str] = Header(default=None),
    settings: JWTSettings = Depends(get_jwt_settings),
) -> Tuple[User, Optional[TokenPayload]]:
    """Get User and TokenPayload from authentication. TokenPayload is None for API key auth."""
    user = get_authenticated_user(auth_result, session)
    token_payload = None
    
    if auth_result["mode"] == "jwt":
        # Re-verify JWT to get token payload
        try:
            token = _decode_authorization_header(authorization)
            token_payload = _verify_jwt_token(token, settings)
        except:
            pass  # If it fails, token_payload remains None
    
    return user, token_payload


def require_roles(*required_roles: Role) -> Callable:
    """Authorization dependency that works with both JWT and API key authentication."""
    
    if not required_roles:
        raise ValueError("At least one role must be provided")
    
    def dependency(
        auth_result: dict = Depends(auth_user_or_api_key),
        session: Session = Depends(get_session),
    ) -> User:
        mode = auth_result["mode"]
        is_dev = auth_result.get("is_dev", False)
        env_dev = os.getenv("ENV", "").upper() == "DEV"
        
        if mode == "jwt":
            # JWT authentication - check user roles from database
            user = auth_result["user"]
            user_roles = set(user.roles or [])
            
            if user_roles & PRIVILEGED_ROLES:
                return user
            
            if not any(role in user_roles for role in required_roles):
                raise_api_error(
                    code=ErrorCodes.AUTH_ERROR,
                    error=ErrorCodes.AUTH_ERROR_A01,
                    detail="Insufficient permissions",
                    status=status.HTTP_403_FORBIDDEN,
                )
        
        elif mode == "api_key":
            # API key authentication - check API key roles
            api_key = auth_result["api_key"]
            api_key_roles = set(api_key.roles or [])
            
            # Check if API key has privileged roles
            if api_key_roles & PRIVILEGED_ROLES:
                # Look up user to return
                statement = select(User).where(User.github_user_name == api_key.github_username)
                user = session.exec(statement).first()
                if not user:
                    raise_api_error(
                        code=ErrorCodes.AUTH_ERROR,
                        error=ErrorCodes.AUTH_ERROR_A01,
                        detail="User associated with API key not found",
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
                user.roles = user.roles or []
                return user
            
            # If ENV=DEV, grant full access (dev environment allows all API keys)
            if env_dev:
                # Still need to return a User object, so look it up
                statement = select(User).where(User.github_user_name == api_key.github_username)
                user = session.exec(statement).first()
                if not user:
                    raise_api_error(
                        code=ErrorCodes.AUTH_ERROR,
                        error=ErrorCodes.AUTH_ERROR_A01,
                        detail="User associated with API key not found",
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
                user.roles = user.roles or []
                return user
            
            # Otherwise check if any required role is in API key roles
            if not any(role in api_key_roles for role in required_roles):
                raise_api_error(
                    code=ErrorCodes.AUTH_ERROR,
                    error=ErrorCodes.AUTH_ERROR_A01,
                    detail="Insufficient permissions",
                    status=status.HTTP_403_FORBIDDEN,
                )
            
            # Look up user to return
            statement = select(User).where(User.github_user_name == api_key.github_username)
            user = session.exec(statement).first()
            if not user:
                raise_api_error(
                    code=ErrorCodes.AUTH_ERROR,
                    error=ErrorCodes.AUTH_ERROR_A01,
                    detail="User associated with API key not found",
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            user.roles = user.roles or []
            return user
        
        raise_api_error(
            code=ErrorCodes.AUTH_ERROR,
            error=ErrorCodes.AUTH_ERROR_A01,
            detail="Invalid authentication",
            status=status.HTTP_401_UNAUTHORIZED,
        )
    
    return dependency

