from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, validator

# ----------------------
# Input DTOs
# ----------------------
class CreateProfile(BaseModel):
    """``username`` must match an existing ``User.github_user_name``."""
    username: str

    @validator("username")
    def username_non_empty(cls, v: str) -> str:
        if not v or not str(v).strip():
            raise ValueError("username cannot be empty")
        return str(v).strip()


class UpdateProfile(BaseModel):
    username: Optional[str] = None

    @validator("username")
    def username_non_empty_when_set(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not str(v).strip():
            raise ValueError("username cannot be empty")
        return str(v).strip()


# ----------------------
# Output DTO
# ----------------------
class ReadProfile(BaseModel):
    id: UUID
    user_id: UUID
    username: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Note: Extended DTOs (ReadProfileWithUser, ReadProfileFull) are in extended_entities.py
# to avoid circular import issues