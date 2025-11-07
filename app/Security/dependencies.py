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
    roles: List[Role] = Field(default_factory=list)
    expires_at: datetime = Field(alias="exp")

    @field_validator("expires_at", mode="before")
    @classmethod
    def _convert_exp(cls, value: object) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(value, tz=timezone.utc)
        raise ValueError("Invalid expiration claim")

    @field_validator("roles", mode="before")
    @classmethod
    def _parse_roles(cls, value: object) -> List[Role]:
        if value is None:
            return []
        if isinstance(value, Role):
            return [value]
        if isinstance(value, str):
            value = [value]
        if not isinstance(value, Iterable):
            raise ValueError("Roles must be iterable")
        parsed: List[Role] = []
        for raw_role in value:
            if isinstance(raw_role, Role):
                parsed.append(raw_role)
                continue
            try:
                parsed.append(Role(raw_role))
            except ValueError as exc:  # pragma: no cover - defensive
                raise ValueError(f"Unknown role: {raw_role}") from exc
        return parsed


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


def verify_nextauth_jwt(
    authorization: Optional[str] = Header(default=None),
    settings: JWTSettings = Depends(get_jwt_settings),
) -> TokenPayload:
    """Validate an incoming NextAuth JWT and return its payload."""

    token = _decode_authorization_header(authorization)
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


PRIVILEGED_ROLES = {Role.GLOBAL_ADMIN, Role.LOCAL_ADMIN}


def require_roles(*required_roles: Role) -> Callable[[User], User]:
    """Return a dependency enforcing that the user has the required role(s)."""

    if not required_roles:
        raise ValueError("At least one role must be provided")

    def dependency(current_user: User = Depends(get_current_user)) -> User:
        user_roles = set(current_user.roles or [])
        if user_roles & PRIVILEGED_ROLES:
            return current_user
        if not any(role in user_roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user

    return dependency

