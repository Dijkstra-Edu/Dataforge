from __future__ import annotations

from typing import Optional, List, Annotated
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

from Schema.SQL.Enums.enums import SchoolType, WorkLocationType, Tools, Degree

class CreateEducation(BaseModel):
    profile_id: UUID
    school_name: Annotated[str, Field(min_length=1, strip_whitespace=True)]
    school_logo_url: Optional[str] = None
    school_type: SchoolType
    degree: Degree
    course_field_name: Annotated[str, Field(min_length=1, strip_whitespace=True)]
    currently_studying: bool
    location: Optional[CreateLocation] = None
    location_type: WorkLocationType
    start_date_month: Annotated[int, Field(ge=1, le=12)]
    start_date_year: int
    end_date_month: Optional[Annotated[int, Field(ge=1, le=12)]] = None
    end_date_year: Optional[int] = None
    description_general: str
    description_detailed: Optional[str] = None
    description_less: Optional[str] = None
    work_done: Optional[str] = None
    school_score_multiplier: Optional[float] = None
    cgpa: Optional[float] = None
    tools_used: Optional[List[Tools]] = None


class UpdateEducation(BaseModel):
    school_name: Optional[Annotated[str, Field(min_length=1, strip_whitespace=True)]] = None
    school_logo_url: Optional[str] = None
    school_type: Optional[SchoolType] = None
    degree: Optional[Degree] = None
    course_field_name: Optional[Annotated[str, Field(min_length=1, strip_whitespace=True)]] = None
    currently_studying: Optional[bool] = None
    location: Optional[CreateLocation] = None
    location_type: Optional[WorkLocationType] = None
    start_date_month: Optional[Annotated[int, Field(ge=1, le=12)]] = None
    start_date_year: Optional[int] = None
    end_date_month: Optional[Annotated[int, Field(ge=1, le=12)]] = None
    end_date_year: Optional[int] = None
    description_general: Optional[str] = None
    description_detailed: Optional[str] = None
    description_less: Optional[str] = None
    work_done: Optional[str] = None
    school_score_multiplier: Optional[float] = None
    cgpa: Optional[float] = None
    tools_used: Optional[List[Tools]] = None

class ReadEducation(BaseModel):
    id: UUID
    profile_id: UUID
    school_name: str
    school_logo_url: Optional[str]
    school_type: SchoolType
    degree: Degree
    course_field_name: str
    currently_studying: bool
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
    school_score_multiplier: Optional[float]
    cgpa: Optional[float]
    tools_used: Optional[List[Tools]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Import at the end to avoid circular imports
from Entities.UserDTOs.location_entity import CreateLocation, ReadLocation


class ReadEducationWithLocation(ReadEducation):
    location_rel: Optional[ReadLocation] = None
    
    class Config:
        from_attributes = True