from typing import Optional, List, TYPE_CHECKING
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, field_validator

from Schema.SQL.Enums.enums import SchoolType, WorkLocationType, Tools, Degree

if TYPE_CHECKING:
    from Entities.UserDTOs.location_entity import ReadLocation

class CreateEducation(BaseModel):
    profile_id: UUID
    school_name: str
    school_logo_url: Optional[str] = None
    school_type: SchoolType
    degree: Degree
    course_field_name: str
    currently_studying: bool
    location: UUID
    location_type: WorkLocationType
    start_date_month: int
    start_date_year: int
    end_date_month: Optional[int] = None
    end_date_year: Optional[int] = None
    description_general: str
    description_detailed: Optional[str] = None
    description_less: Optional[str] = None
    work_done: Optional[str] = None
    school_score_multiplier: Optional[float] = None
    cgpa: Optional[float] = None
    tools_used: Optional[List[Tools]] = None

    @field_validator("school_name")
    def school_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("school_name cannot be empty")
        return v.strip()

    @field_validator("course_field_name")
    def field_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("course_field_name cannot be empty")
        return v.strip()

    @field_validator("start_date_month", "end_date_month")
    def validate_month(cls, v):
        if v is not None and (v < 1 or v > 12):
            raise ValueError("Month must be between 1 and 12")
        return v


class UpdateEducation(BaseModel):
    school_name: Optional[str] = None
    school_logo_url: Optional[str] = None
    school_type: Optional[SchoolType] = None
    degree: Optional[Degree] = None
    course_field_name: Optional[str] = None
    currently_studying: Optional[bool] = None
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
    school_score_multiplier: Optional[float] = None
    cgpa: Optional[float] = None
    tools_used: Optional[List[Tools]] = None

    @field_validator("school_name")
    def school_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("school_name cannot be empty")
        return v.strip() if v else v

    @field_validator("course_field_name")
    def field_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("course_field_name cannot be empty")
        return v.strip() if v else v

    @field_validator("start_date_month", "end_date_month")
    def validate_month(cls, v):
        if v is not None and (v < 1 or v > 12):
            raise ValueError("Month must be between 1 and 12")
        return v

class ReadEducation(BaseModel):
    id: UUID
    profile_id: UUID
    school_name: str
    school_logo_url: Optional[str]
    school_type: SchoolType
    degree: Degree
    course_field_name: str
    currently_studying: bool
    location: UUID
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


class ReadEducationWithLocation(ReadEducation):
    location_rel: Optional['ReadLocation'] = None
    
    class Config:
        from_attributes = True