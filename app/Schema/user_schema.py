# Schema/users_schema.py

from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from Entities.SQL.Enums.enums import Rank

# ----------------------
# Input DTOs
# ----------------------
class CreateUser(BaseModel):
    github_user_name: str
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    rank: Optional[Rank] = Rank.UNRANKED
    streak: Optional[int] = None


class UpdateUser(BaseModel):
    github_user_name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    rank: Optional[Rank] = None
    streak: Optional[int] = None


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
