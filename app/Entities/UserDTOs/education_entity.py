from typing import Optional, List
from uuid import UUID
from datetime import datetime, date
from pydantic import BaseModel, field_validator

from Schema.SQL.Enums.enums import WorkLocationType, Tools

class CreateEducation(BaseModel):
    profile_id: UUID
    school: str
    school_type: str
    degree: str
    field: str
    currently_studying: bool
    location: UUID
    location_type: WorkLocationType
    start_date: date
    end_date: Optional[date] = None
    description_general: str
    description_detailed: Optional[str] = None
    description_less: Optional[str] = None
    work_done: Optional[str] = None
    school_score_multiplier: Optional[float] = None
    tools_used: Optional[List[Tools]] = None

    @field_validator("school")
    def school_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("school cannot be empty")
        return v.strip()

    @field_validator("degree")
    def degree_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("degree cannot be empty")
        return v.strip()


class UpdateEducation(BaseModel):
    school: Optional[str] = None
    school_type: Optional[str] = None
    degree: Optional[str] = None
    field: Optional[str] = None
    currently_studying: Optional[bool] = None
    location: Optional[UUID] = None
    location_type: Optional[WorkLocationType] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description_general: Optional[str] = None
    description_detailed: Optional[str] = None
    description_less: Optional[str] = None
    work_done: Optional[str] = None
    school_score_multiplier: Optional[float] = None
    tools_used: Optional[List[Tools]] = None

    @field_validator("school")
    def school_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("school cannot be empty")
        return v.strip() if v else v

    @field_validator("degree")
    def degree_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("degree cannot be empty")
        return v.strip() if v else v

class ReadEducation(BaseModel):
    id: UUID
    profile_id: UUID
    school: str
    school_type: str
    degree: str
    field: str
    currently_studying: bool
    location: UUID
    location_type: WorkLocationType
    start_date: date
    end_date: Optional[date]
    description_general: str
    description_detailed: Optional[str]
    description_less: Optional[str]
    work_done: Optional[str]
    school_score_multiplier: Optional[float]
    tools_used: Optional[List[Tools]]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
