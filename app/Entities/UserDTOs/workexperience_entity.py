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
    company_logo: Optional[str] = None
    currently_working: bool
    location: Optional[UUID] = None
    location_type: WorkLocationType
    start_date_month: int
    start_date_year: int
    end_date_month: Optional[int] = None
    end_date_year: Optional[int] = None
    description_general: str
    description_detailed: Optional[str] = None
    description_less: Optional[str] = None
    work_done: Optional[str] = None
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

    @field_validator('start_date_month')
    def validate_start_month(cls, v):
        if v < 1 or v > 12:
            raise ValueError('start_date_month must be between 1 and 12')
        return v

    @field_validator('end_date_month')
    def validate_end_month(cls, v):
        if v is not None and (v < 1 or v > 12):
            raise ValueError('end_date_month must be between 1 and 12')
        return v

    @field_validator('end_date_year')
    def validate_end_date(cls, v, values):
        if v is not None:
            start_year = values.data.get('start_date_year')
            start_month = values.data.get('start_date_month')
            end_month = values.data.get('end_date_month')
            
            if start_year and start_month and end_month:
                if v < start_year or (v == start_year and end_month < start_month):
                    raise ValueError('end_date cannot be before start_date')
        return v


class UpdateWorkExperience(BaseModel):
    profile_id: Optional[UUID] = None
    title: Optional[str] = None
    employment_type: Optional[EmploymentType] = None
    domain: Optional[List[Domain]] = None
    company_name: Optional[str] = None
    company_logo: Optional[str] = None
    currently_working: Optional[bool] = None
    location: Optional[UUID] = None
    location_type: Optional[WorkLocationType] = None
    start_date_month: Optional[int] = None
    start_date_year: Optional[int] = None
    end_date_month: Optional[int] = None
    end_date_year: Optional[int] = None
    description_general: Optional[str] = None
    description_detailed: Optional[str] = None
    description_less: Optional[str] = None
    work_done: Optional[str] = None
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

    @field_validator('start_date_month')
    def validate_start_month(cls, v):
        if v is not None and (v < 1 or v > 12):
            raise ValueError('start_date_month must be between 1 and 12')
        return v

    @field_validator('end_date_month')
    def validate_end_month(cls, v):
        if v is not None and (v < 1 or v > 12):
            raise ValueError('end_date_month must be between 1 and 12')
        return v

    @field_validator('end_date_year')
    def validate_end_date(cls, v, values):
        if v is not None:
            start_year = values.data.get('start_date_year')
            start_month = values.data.get('start_date_month')
            end_month = values.data.get('end_date_month')
            
            if start_year and start_month and end_month:
                if v < start_year or (v == start_year and end_month < start_month):
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
    company_logo: Optional[str]
    currently_working: bool
    location: Optional[UUID]
    location_type: WorkLocationType
    start_date_month: int
    start_date_year: int
    end_date_month: Optional[int]
    end_date_year: Optional[int]
    description_general: str
    description_detailed: Optional[str]
    description_less: Optional[str]
    work_done: Optional[str]
    company_score: Optional[float]
    time_spent_multiplier: Optional[float]
    work_done_multiplier: Optional[float]
    tools_used: Optional[List[Tools]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ----------------------
# Extended Output DTO with related entities
# ----------------------
class ReadWorkExperienceWithRelations(ReadWorkExperience):
    profile: Optional['ReadProfile'] = None
    location_rel: Optional['ReadLocation'] = None

    class Config:
        from_attributes = True


# Import here to avoid circular imports
from Entities.UserDTOs.profile_entity import ReadProfile
from Entities.UserDTOs.location_entity import ReadLocation
ReadWorkExperienceWithRelations.model_rebuild()