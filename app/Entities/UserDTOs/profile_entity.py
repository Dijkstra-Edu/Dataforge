from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

# ----------------------
# Input DTOs
# ----------------------
class CreateProfile(BaseModel):
    user_id: UUID


class UpdateProfile(BaseModel):
    user_id: Optional[UUID] = None


# ----------------------
# Output DTO
# ----------------------
class ReadProfile(BaseModel):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Note: Extended DTOs (ReadProfileWithUser, ReadProfileFull) are in extended_entities.py
# to avoid circular import issues