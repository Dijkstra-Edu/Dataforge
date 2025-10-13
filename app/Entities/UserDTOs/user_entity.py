from typing import Optional, List, TYPE_CHECKING
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, field_validator

from Schema.SQL.Enums.enums import Rank, Domain

if TYPE_CHECKING:
    from Entities.UserDTOs.links_entity import ReadLinks
    from Entities.UserDTOs.profile_entity import ReadProfileFull

# ----------------------
# Input DTOs
# ----------------------
class CreateUser(BaseModel):
    github_user_name: str
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    rank: Rank = Rank.UNRANKED
    streak: Optional[int] = None
    primary_specialization: Domain
    secondary_specializations: List[Domain]
    expected_salary_bucket: Rank
    time_left: int
    onboarding_complete: bool = False
    data_loaded: bool = False

    @field_validator('github_user_name')
    def github_user_name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('github_user_name cannot be empty')
        return v.strip()

    @field_validator('first_name')
    def first_name_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('first_name cannot be empty string')
        return v.strip() if v else v

    @field_validator('last_name')
    def last_name_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('last_name cannot be empty string')
        return v.strip() if v else v


class UpdateUser(BaseModel):
    github_user_name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    rank: Optional[Rank] = None
    streak: Optional[int] = None
    primary_specialization: Optional[Domain] = None
    secondary_specializations: Optional[List[Domain]] = None
    expected_salary_bucket: Optional[Rank] = None
    time_left: Optional[int] = None
    onboarding_complete: Optional[bool] = None
    data_loaded: Optional[bool] = None

    @field_validator('github_user_name')
    def github_user_name_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('github_user_name cannot be empty')
        return v.strip() if v else v

    @field_validator('first_name')
    def first_name_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('first_name cannot be empty string')
        return v.strip() if v else v

    @field_validator('last_name')
    def last_name_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('last_name cannot be empty string')
        return v.strip() if v else v


# ----------------------
# Output DTO
# ----------------------
class ReadUser(BaseModel):
    id: UUID
    github_user_name: str
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    rank: Rank
    streak: Optional[int]
    primary_specialization: Domain
    secondary_specializations: List[Domain]
    expected_salary_bucket: Rank
    time_left: int
    onboarding_complete: bool
    data_loaded: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ----------------------
# Onboarding DTOs
# ----------------------
class OnboardUser(BaseModel):
    github_user_name: str
    linkedin_user_name: str
    leetcode_user_name: str
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    rank: Rank = Rank.UNRANKED
    streak: int = 0
    primary_specialization: Domain
    secondary_specializations: List[Domain]
    expected_salary_bucket: Rank
    time_left: int

    @field_validator('github_user_name', 'linkedin_user_name', 'leetcode_user_name')
    def usernames_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('username cannot be empty')
        return v.strip()

    @field_validator('first_name')
    def first_name_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('first_name cannot be empty string')
        return v.strip() if v else v

    @field_validator('last_name')
    def last_name_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('last_name cannot be empty string')
        return v.strip() if v else v


class OnboardCheckResponse(BaseModel):
    onboarded: bool
    user_id: Optional[UUID] = None


# ----------------------
# Extended Output DTO with full nested data
# ----------------------
class ReadUserFull(ReadUser):
    links: Optional['ReadLinks'] = None
    profile: Optional['ReadProfileFull'] = None
    
    class Config:
        from_attributes = True