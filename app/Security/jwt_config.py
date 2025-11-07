from functools import lru_cache
from typing import List, Optional

from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv
import os
from Utils.errors import raise_api_error
from Utils.error_codes import ErrorCodes

load_dotenv()

NEXTAUTH_SECRET = os.getenv("NEXTAUTH_SECRET") if os.getenv("NEXTAUTH_SECRET") else raise_api_error(ErrorCodes.AUTH_ERROR, ErrorCodes.AUTH_ERROR_A01, "NEXTAUTH_SECRET is not set")
NEXTAUTH_ALGORITHMS = os.getenv("NEXTAUTH_ALGORITHMS") if os.getenv("NEXTAUTH_ALGORITHMS") else ["HS256"]
NEXTAUTH_ISSUER = os.getenv("NEXTAUTH_ISSUER") if os.getenv("NEXTAUTH_ISSUER") else None
NEXTAUTH_AUDIENCE = os.getenv("NEXTAUTH_AUDIENCE") if os.getenv("NEXTAUTH_AUDIENCE") else None

class JWTSettings(BaseSettings):
    """Configuration for validating NextAuth-issued JWT tokens."""

    nextauth_secret: str = Field(..., env="NEXTAUTH_SECRET")
    algorithms: List[str] = Field(default_factory=lambda: NEXTAUTH_ALGORITHMS)
    issuer: Optional[str] = Field(default=None, env="NEXTAUTH_ISSUER")
    audience: Optional[str] = Field(default=None, env="NEXTAUTH_AUDIENCE")


@lru_cache
def get_jwt_settings() -> JWTSettings:
    """Return cached JWT settings loaded from the environment."""

    return JWTSettings()


def reset_jwt_settings_cache() -> None:
    """Clear the cached JWT settings (useful for tests)."""

    get_jwt_settings.cache_clear()

