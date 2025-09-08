from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, validator

# ----------------------
# Input DTOs
# ----------------------
class CreateProfile(BaseModel):
    user_id: UUID

    @validator('user_id')
    def user_id_must_be_valid_uuid(cls, v):
        if not v:
            raise ValueError('user_id cannot be empty')
        return v


class UpdateProfile(BaseModel):
    user_id: Optional[UUID] = None

    @validator('user_id')
    def user_id_must_be_valid_uuid(cls, v):
        if v is not None and not v:
            raise ValueError('user_id cannot be empty')
        return v


# ----------------------
# Output DTO
# ----------------------
class ReadProfile(BaseModel):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ----------------------
# Extended Output DTO with User details
# ----------------------
class ReadProfileWithUser(ReadProfile):
    user: Optional['ReadUser'] = None

    class Config:
        orm_mode = True


# Import here to avoid circular imports
from Schema.user_schema import ReadUser
ReadProfileWithUser.update_forward_refs()