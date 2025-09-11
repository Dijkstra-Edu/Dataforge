from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, field_validator

from Schema.SQL.Models.models import Rank

# ----------------------
# Input DTOs
# ----------------------
class CreateUser(BaseModel):
    github_user_name: str
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    rank: Rank = Rank.UNRANKED
    streak: Optional[int] = None

    @field_validator('github_user_name')
    def github_user_name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('github_user_name cannot be empty')
        return v.strip()

    @field_validator('first_name')
    def first_name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('first_name cannot be empty')
        return v.strip()

    @field_validator('last_name')
    def last_name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('last_name cannot be empty')
        return v.strip()


class UpdateUser(BaseModel):
    github_user_name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    rank: Optional[Rank] = None
    streak: Optional[int] = None

    @field_validator('github_user_name')
    def github_user_name_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('github_user_name cannot be empty')
        return v.strip() if v else v

    @field_validator('first_name')
    def first_name_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('first_name cannot be empty')
        return v.strip() if v else v

    @field_validator('last_name')
    def last_name_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('last_name cannot be empty')
        return v.strip() if v else v


# ----------------------
# Output DTO
# ----------------------
class ReadUser(BaseModel):
    id: UUID
    github_user_name: str
    first_name: str
    middle_name: Optional[str]
    last_name: str
    rank: Rank
    streak: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True