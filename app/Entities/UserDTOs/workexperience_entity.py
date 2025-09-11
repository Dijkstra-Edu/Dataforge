from typing import Optional, List
from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel, field_validator

from Schema.SQL.Enums.enums import EmploymentType, WorkLocationType, Domain, Tools

# ----------------------
# Input DTOs
# ----------------------
class CreateWorkExperience(BaseModel):
    profile_id: UUID
    title: str
    employment_type: EmploymentType
    domain: Optional[List[Domain]] = None
    company_name: str
    currently_working: bool
    location: UUID
    location_type: WorkLocationType
    start_date: date
    end_date: Optional[date] = None
    description_general: str
    description_detailed: Optional[str] = None
    description_less: Optional[str] = None
    work_done: List[str]
    company_score: Optional[float] = None
    time_spent_multiplier: Optional[float] = None
    work_done_multiplier: Optional[float] = None
    tools_used: Optional[List[Tools]] = None

    @field_validator('title')
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('title cannot be empty')
        return v.strip()

    @field_validator('company_name')
    def company_name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('company_name cannot be empty')
        return v.strip()

    @field_validator('description_general')
    def description_general_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('description_general cannot be empty')
        return v.strip()

    @field_validator('work_done')
    def work_done_must_not_be_empty(cls, v):
        if not v or len(v) == 0:
            raise ValueError('work_done cannot be empty')
        return v

    @field_validator('end_date')
    def validate_end_date(cls, v, values):
        if v and 'start_date' in values and v < values['start_date']:
            raise ValueError('end_date cannot be before start_date')
        return v


class UpdateWorkExperience(BaseModel):
    profile_id: Optional[UUID] = None
    title: Optional[str] = None
    employment_type: Optional[EmploymentType] = None
    domain: Optional[List[Domain]] = None
    company_name: Optional[str] = None
    currently_working: Optional[bool] = None
    location: Optional[UUID] = None
    location_type: Optional[WorkLocationType] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description_general: Optional[str] = None
    description_detailed: Optional[str] = None
    description_less: Optional[str] = None
    work_done: Optional[List[str]] = None
    company_score: Optional[float] = None
    time_spent_multiplier: Optional[float] = None
    work_done_multiplier: Optional[float] = None
    tools_used: Optional[List[Tools]] = None

    @field_validator('title')
    def title_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('title cannot be empty')
        return v.strip() if v else v

    @field_validator('company_name')
    def company_name_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('company_name cannot be empty')
        return v.strip() if v else v

    @field_validator('description_general')
    def description_general_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('description_general cannot be empty')
        return v.strip() if v else v

    @field_validator('work_done')
    def work_done_must_not_be_empty(cls, v):
        if v is not None and len(v) == 0:
            raise ValueError('work_done cannot be empty')
        return v

    @field_validator('end_date')
    def validate_end_date(cls, v, values):
        if v and 'start_date' in values and values['start_date'] and v < values['start_date']:
            raise ValueError('end_date cannot be before start_date')
        return v


# ----------------------
# Output DTO
# ----------------------
class ReadWorkExperience(BaseModel):
    id: UUID
    profile_id: UUID
    title: str
    employment_type: EmploymentType
    domain: Optional[List[Domain]]
    company_name: str
    currently_working: bool
    location: UUID
    location_type: WorkLocationType
    start_date: date
    end_date: Optional[date]
    description_general: str
    description_detailed: Optional[str]
    description_less: Optional[str]
    work_done: List[str]
    company_score: Optional[float]
    time_spent_multiplier: Optional[float]
    work_done_multiplier: Optional[float]
    tools_used: Optional[List[Tools]]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ----------------------
# Extended Output DTO with related entities
# ----------------------
class ReadWorkExperienceWithRelations(ReadWorkExperience):
    profile: Optional['ReadProfile'] = None
    location_rel: Optional['ReadLocation'] = None

    class Config:
        orm_mode = True


# Import here to avoid circular imports
from Entities.UserDTOs.profile_entity import ReadProfile
from Entities.UserDTOs.location_entity import ReadLocation
ReadWorkExperienceWithRelations.model_rebuild()