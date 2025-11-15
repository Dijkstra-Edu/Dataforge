"""Security utilities for authentication and authorization."""

# JWT Dependencies
from Security.jwt_dependencies import (
    TokenPayload,
    verify_nextauth_jwt,
    get_current_user,
    get_current_user_with_token,
    auth_jwt_required,
    PRIVILEGED_ROLES,
)

# API Key Dependencies
from Security.api_key_dependencies import (
    verify_api_key,
    auth_api_key_required,
)

# Unified Dependencies
from Security.unified_dependencies import (
    auth_user_or_api_key,
    get_authenticated_user,
    get_authenticated_user_with_token,
    require_roles,
)

__all__ = [
    # JWT
    "TokenPayload",
    "verify_nextauth_jwt",
    "get_current_user",
    "get_current_user_with_token",
    "auth_jwt_required",
    "PRIVILEGED_ROLES",
    # API Key
    "verify_api_key",
    "auth_api_key_required",
    # Unified
    "auth_user_or_api_key",
    "get_authenticated_user",
    "get_authenticated_user_with_token",
    "require_roles",
]
