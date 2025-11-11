from __future__ import annotations

from typing import Optional, List, Annotated
from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel, field_validator, Field

from Schema.SQL.Enums.enums import EmploymentType, WorkLocationType, Domain, Tools
from Entities.UserDTOs.location_entity import CreateLocation, ReadLocation

# ----------------------
# Input DTOs
# ----------------------
class CreateWorkExperience(BaseModel):
    profile_id: UUID
    title: Annotated[str, Field(min_length=1, strip_whitespace=True)]
    employment_type: EmploymentType
    domain: Optional[List[Domain]] = None
    company_name: Annotated[str, Field(min_length=1, strip_whitespace=True)]
    company_logo: Optional[str] = None
    currently_working: bool
    location: Optional[CreateLocation] = None
    location_type: WorkLocationType
    start_date_month: Annotated[int, Field(ge=1, le=12)]
    start_date_year: int
    end_date_month: Optional[Annotated[int, Field(ge=1, le=12)]] = None
    end_date_year: Optional[int] = None
    description_general: Annotated[str, Field(min_length=1, strip_whitespace=True)]
    description_detailed: Optional[str] = None
    description_less: Optional[str] = None
    work_done: Optional[str] = None
    company_score: Optional[float] = None
    time_spent_multiplier: Optional[float] = None
    work_done_multiplier: Optional[float] = None
    tools_used: Optional[List[Tools]] = None

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
    title: Optional[Annotated[str, Field(min_length=1, strip_whitespace=True)]] = None
    employment_type: Optional[EmploymentType] = None
    domain: Optional[List[Domain]] = None
    company_name: Optional[Annotated[str, Field(min_length=1, strip_whitespace=True)]] = None
    company_logo: Optional[str] = None
    currently_working: Optional[bool] = None
    location: Optional[CreateLocation] = None
    location_type: Optional[WorkLocationType] = None
    start_date_month: Optional[Annotated[int, Field(ge=1, le=12)]] = None
    start_date_year: Optional[int] = None
    end_date_month: Optional[Annotated[int, Field(ge=1, le=12)]] = None
    end_date_year: Optional[int] = None
    description_general: Optional[Annotated[str, Field(min_length=1, strip_whitespace=True)]] = None
    description_detailed: Optional[str] = None
    description_less: Optional[str] = None
    work_done: Optional[str] = None
    company_score: Optional[float] = None
    time_spent_multiplier: Optional[float] = None
    work_done_multiplier: Optional[float] = None
    tools_used: Optional[List[Tools]] = None

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
    location: Optional[ReadLocation]
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


# Import at the end to avoid circular imports
from Entities.UserDTOs.profile_entity import ReadProfile
from Entities.UserDTOs.location_entity import ReadLocation


# ----------------------
# Extended Output DTO with related entities
# ----------------------
class ReadWorkExperienceWithRelations(ReadWorkExperience):
    profile: Optional[ReadProfile] = None
    location_rel: Optional[ReadLocation] = None

    class Config:
        from_attributes = True


class ReadWorkExperienceWithLocation(ReadWorkExperience):
    location_rel: Optional[ReadLocation] = None
    
    class Config:
        from_attributes = True