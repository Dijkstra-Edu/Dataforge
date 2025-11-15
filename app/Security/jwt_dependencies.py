from datetime import datetime, timezone
from typing import Callable, Iterable, List, Optional

from fastapi import Depends, Header, HTTPException, status
from jose import JWTError, jwt
from pydantic import BaseModel, Field, ValidationError, field_validator
from sqlmodel import Session, select

from Schema.SQL.Enums.enums import Role
from Schema.SQL.Models.models import User
from Security.jwt_config import JWTSettings, get_jwt_settings
from Utils.error_codes import ErrorCodes
from Utils.errors import raise_api_error
from db import get_session


class TokenPayload(BaseModel):
    """Represents the claims expected in a NextAuth JWT."""

    subject: Optional[str] = Field(default=None, alias="sub")
    github_username: str = Field(alias="githubUsername")
    expires_at: datetime = Field(alias="exp")
    is_dev: Optional[bool] = Field(default=False, alias="isDev")

    @field_validator("expires_at", mode="before")
    @classmethod
    def _convert_exp(cls, value: object) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(value, tz=timezone.utc)
        raise ValueError("Invalid expiration claim")


def _decode_authorization_header(
    authorization: Optional[str],
) -> str:
    if not authorization:
        raise raise_api_error(
            code=ErrorCodes.AUTH_ERROR,
            error=ErrorCodes.AUTH_ERROR_A01,   
            detail="Missing Authorization header",
            status=status.HTTP_401_UNAUTHORIZED,
        )
    if not authorization.startswith("Bearer "):
        raise raise_api_error(
            code=ErrorCodes.AUTH_ERROR,
            error=ErrorCodes.AUTH_ERROR_A02,
            detail="Authorization header must start with Bearer",
            status=status.HTTP_401_UNAUTHORIZED,
        )
    token = authorization.removeprefix("Bearer ").strip()
    if not token:
        raise raise_api_error(
            code=ErrorCodes.AUTH_ERROR,
            error=ErrorCodes.AUTH_ERROR_A03,
            detail="Bearer token is empty",
            status=status.HTTP_401_UNAUTHORIZED,
        )
    return token


def _verify_jwt_token(
    token: str,
    settings: JWTSettings,
) -> TokenPayload:
    """Core JWT verification logic without dependency injection."""
    options = {"verify_aud": settings.audience is not None}
    try:
        payload = jwt.decode(
            token,
            settings.nextauth_secret,
            algorithms=settings.algorithms,
            audience=settings.audience,
            issuer=settings.issuer,
            options=options,
        )
        token_payload = TokenPayload.model_validate(payload)
    except (JWTError, ValidationError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        ) from exc

    if token_payload.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )

    return token_payload


def verify_nextauth_jwt(
    authorization: Optional[str] = Header(default=None),
    settings: JWTSettings = Depends(get_jwt_settings),
) -> TokenPayload:
    """Validate an incoming NextAuth JWT and return its payload."""
    token = _decode_authorization_header(authorization)
    return _verify_jwt_token(token, settings)


def get_current_user(
    token_payload: TokenPayload = Depends(verify_nextauth_jwt),
    session: Session = Depends(get_session),
) -> User:
    """Fetch the authenticated user from the database."""

    statement = select(User).where(User.github_user_name == token_payload.github_username)
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticated user record not found",
        )

    user.roles = user.roles or []
    return user


def get_current_user_with_token(
    token_payload: TokenPayload = Depends(verify_nextauth_jwt),
    session: Session = Depends(get_session),
) -> tuple[User, TokenPayload]:
    """Fetch the authenticated user and return both user and token payload."""
    user = get_current_user(token_payload, session)
    return user, token_payload


PRIVILEGED_ROLES = {Role.GLOBAL_ADMIN, Role.LOCAL_ADMIN}


def auth_jwt_required(
    current_user: User = Depends(get_current_user),
) -> User:
    """JWT-only authentication dependency."""
    return current_user

