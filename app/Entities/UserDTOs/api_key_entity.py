from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from Schema.SQL.Enums.enums import Role

# ----------------------
# Input DTOs
# ----------------------
class CreateAPIKey(BaseModel):
    description: Optional[str] = None
    expires_in: Optional[datetime] = None
    roles: List[Role]

# ----------------------
# Output DTOs
# ----------------------
class ReadAPIKey(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    expires_in: Optional[datetime]
    github_username: str
    description: Optional[str]
    active: bool
    roles: List[Role]

    class Config:
        from_attributes = True

class UpdateAPIKey(BaseModel):
    description: Optional[str] = None
    active: Optional[bool] = None
    roles: Optional[List[Role]] = None

class APIKeyResponse(BaseModel):
    """Response returned only when creating an API key - includes the plain key."""
    key: str
    created_at: datetime
    expires_in: Optional[datetime]
    description: Optional[str]
    roles: List[Role]

