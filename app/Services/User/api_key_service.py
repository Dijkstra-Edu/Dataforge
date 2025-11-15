import secrets
import hashlib
from typing import List
from uuid import UUID
from datetime import datetime, timezone
from sqlmodel import Session

from Schema.SQL.Enums.enums import Role
from Schema.SQL.Models.models import APIKey
from Repository.User.api_key_repository import APIKeyRepository
from Entities.UserDTOs.api_key_entity import CreateAPIKey, ReadAPIKey, UpdateAPIKey, APIKeyResponse
from Utils.Exceptions.user_exceptions import (
    APIKeyNotFound, APIKeyExpired, APIKeyInactive, InvalidAPIKeyRoles
)

class APIKeyService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = APIKeyRepository(session)

    @staticmethod
    def _generate_key() -> str:
        """Generate API key with DJK_ prefix."""
        token = secrets.token_urlsafe(32)
        return f"DJK_{token}"

    @staticmethod
    def _hash_key(key: str) -> str:
        """Hash API key with SHA256."""
        return hashlib.sha256(key.encode()).hexdigest()

    def _validate_roles(self, requested_roles: List[Role], user_roles: List[Role], is_dev: bool) -> None:
        """Validate that requested roles are subset of user roles (unless is_dev=True)."""
        if is_dev:
            return  # Allow any role in dev mode
        
        user_roles_set = set(user_roles)
        requested_roles_set = set(requested_roles)
        
        if not requested_roles_set.issubset(user_roles_set):
            raise InvalidAPIKeyRoles(list(requested_roles_set), list(user_roles_set))

    def create_api_key(
        self, 
        github_username: str, 
        user_roles: List[Role], 
        is_dev: bool, 
        create_data: CreateAPIKey
    ) -> APIKeyResponse:
        """Create a new API key."""
        # Validate roles
        self._validate_roles(create_data.roles, user_roles, is_dev)
        
        # Generate key and hash
        plain_key = self._generate_key()
        key_hash = self._hash_key(plain_key)
        
        # Create API key record
        api_key = APIKey(
            key_hash=key_hash,
            github_username=github_username,
            description=create_data.description,
            active=True,
            expires_in=create_data.expires_in,
            roles=create_data.roles
        )
        
        created_key = self.repo.create(api_key)
        
        # Return response with plain key (only time it's returned)
        return APIKeyResponse(
            key=plain_key,
            created_at=created_key.created_at,
            expires_in=created_key.expires_in,
            description=created_key.description,
            roles=created_key.roles or []
        )

    def get_api_key(self, api_key_id: UUID, github_username: str) -> ReadAPIKey:
        """Get API key by ID (verify it belongs to user)."""
        api_key = self.repo.get_by_id(api_key_id)
        if not api_key:
            raise APIKeyNotFound(api_key_id)
        
        if api_key.github_username != github_username:
            raise APIKeyNotFound(api_key_id)
        
        return ReadAPIKey.model_validate(api_key)

    def list_api_keys(self, github_username: str) -> List[ReadAPIKey]:
        """List all API keys for a user (without key values)."""
        api_keys = self.repo.list_by_github_username(github_username)
        return [ReadAPIKey.model_validate(key) for key in api_keys]

    def revoke_api_key(self, api_key_id: UUID, github_username: str) -> dict:
        """Revoke (deactivate) an API key."""
        api_key = self.repo.get_by_id(api_key_id)
        if not api_key:
            raise APIKeyNotFound(api_key_id)
        
        if api_key.github_username != github_username:
            raise APIKeyNotFound(api_key_id)
        
        self.repo.revoke(api_key_id)
        return {"status": "revoked", "message": f"API key {api_key_id} has been revoked"}

    def update_api_key(
        self,
        api_key_id: UUID,
        github_username: str,
        user_roles: List[Role],
        is_dev: bool,
        update_data: UpdateAPIKey
    ) -> ReadAPIKey:
        """Update an API key."""
        api_key = self.repo.get_by_id(api_key_id)
        if not api_key:
            raise APIKeyNotFound(api_key_id)
        
        if api_key.github_username != github_username:
            raise APIKeyNotFound(api_key_id)
        
        # Validate roles if being updated
        if update_data.roles is not None:
            self._validate_roles(update_data.roles, user_roles, is_dev)
            api_key.roles = update_data.roles
        
        if update_data.description is not None:
            api_key.description = update_data.description
        
        if update_data.active is not None:
            api_key.active = update_data.active
        
        updated_key = self.repo.update(api_key)
        return ReadAPIKey.model_validate(updated_key)

    def validate_api_key(self, plain_key: str) -> APIKey:
        """Validate an API key and return the APIKey object."""
        key_hash = self._hash_key(plain_key)
        api_key = self.repo.get_active_by_key_hash(key_hash)
        
        if not api_key:
            raise APIKeyNotFound()
        
        # Check expiration
        if api_key.expires_in and api_key.expires_in < datetime.now(timezone.utc):
            raise APIKeyExpired()
        
        # Check active status
        if not api_key.active:
            raise APIKeyInactive()
        
        return api_key

