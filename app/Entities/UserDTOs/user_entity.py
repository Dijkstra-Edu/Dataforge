from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, field_validator

from Schema.SQL.Enums.enums import Rank, Domain, Tools

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
    bio: Optional[str] = None
    location: Optional[UUID] = None
    dream_company: Optional[str] = None
    dream_company_logo: Optional[str] = None
    dream_position: Optional[str] = None
    tools_to_learn: Optional[List[Tools]] = []

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
    bio: Optional[str] = None
    location: Optional[UUID] = None
    dream_company: Optional[str] = None
    dream_company_logo: Optional[str] = None
    dream_position: Optional[str] = None
    tools_to_learn: Optional[List[Tools]] = None

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
    bio: Optional[str]
    location: Optional[UUID]
    dream_company: Optional[str]
    dream_company_logo: Optional[str]
    dream_position: Optional[str]
    tools_to_learn: Optional[List[Tools]]
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
    dream_company: Optional[str] = None
    dream_company_logo: Optional[str] = None
    dream_position: Optional[str] = None
    primary_email: str
    tools_to_learn: Optional[List[Tools]] = []

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

    @field_validator('primary_email')
    def primary_email_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('primary_email cannot be empty')
        return v.strip()


class OnboardCheckResponse(BaseModel):
    onboarded: bool
    user_id: Optional[UUID] = None


# ----------------------
# User Card Details DTO
# ----------------------
class ReadUserCardDetails(BaseModel):
    """User card details including data from User and Links models"""
    github_user_name: str
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    bio: Optional[str]
    rank: Rank
    streak: Optional[int]
    primary_specialization: Domain
    secondary_specializations: List[Domain]
    expected_salary_bucket: Rank
    time_left: int
    linkedin_link: Optional[str]
    portfolio_link: Optional[str]
    leetcode_link: Optional[str]

    class Config:
        from_attributes = True


class ReadUserPersonalDetails(BaseModel):
    """User personal details including data from User and Links models"""
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    bio: Optional[str]
    location_city: Optional[str]
    location_state: Optional[str]
    location_country: Optional[str]
    location_longitude: Optional[float]
    location_latitude: Optional[float]
    primary_email: Optional[str]
    secondary_email: Optional[str]
    school_email: Optional[str]
    work_email: Optional[str]
    portfolio_link: Optional[str]
    github_user_name: str
    linkedin_user_name: Optional[str]
    leetcode_user_name: Optional[str]
    dream_company: Optional[str]
    dream_company_logo: Optional[str]
    dream_position: Optional[str]
    expected_salary_bucket: Rank
    time_left: int
    tools_to_learn: Optional[List[Tools]]
    primary_specialization: Domain
    secondary_specializations: List[Domain]
    rank: Rank
    streak: Optional[int]
    onboarding_complete: bool
    data_loaded: bool
    onboarding_journey_completed: bool

    class Config:
        from_attributes = True

class UpdateUserPersonalDetails(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    location_city: Optional[str] = None
    location_state: Optional[str] = None
    location_country: Optional[str] = None
    location_longitude: Optional[float] = None
    location_latitude: Optional[float] = None
    primary_email: Optional[str] = None
    secondary_email: Optional[str] = None
    school_email: Optional[str] = None
    work_email: Optional[str] = None
    portfolio_link: Optional[str] = None
    linkedin_user_name: Optional[str] = None
    leetcode_user_name: Optional[str] = None
    dream_company: Optional[str] = None
    dream_company_logo: Optional[str] = None
    dream_position: Optional[str] = None
    expected_salary_bucket: Optional[Rank] = None
    time_left: Optional[int] = None
    tools_to_learn: Optional[List[Tools]] = None
    primary_specialization: Optional[Domain] = None
    secondary_specializations: Optional[List[Domain]] = None    

# ----------------------
# User Auth Details DTO
# ----------------------
class ReadUserAuthDetails(BaseModel):
    github_user_name: str
    user_id: UUID
    profile_id: UUID