from typing import Optional, List
from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel, ValidationInfo, field_validator
from Schema.SQL.Enums.enums import (
    Cause,
    Tools,
)  

class CreateVolunteering(BaseModel):
    profile_id: UUID
    organization: str
    role: str
    cause: Cause
    start_date: date
    end_date: Optional[date] = None
    currently_volunteering: bool
    description: Optional[str] = None
    tools: Optional[List[Tools]] = None

    @field_validator("organization")
    def organization_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("organization cannot be empty")
        return v.strip()

    @field_validator("role")
    def role_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("role cannot be empty")
        return v.strip()

    @field_validator("end_date")
    def validate_end_date(cls, v, info: ValidationInfo):
        start_date = info.data.get("start_date")
        if v and start_date and v < start_date:
            raise ValueError("end_date cannot be before start_date")
        return v


class UpdateVolunteering(BaseModel):
    profile_id: Optional[UUID] = None
    organization: Optional[str] = None
    role: Optional[str] = None
    cause: Optional[Cause] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    currently_volunteering: Optional[bool] = None
    description: Optional[str] = None
    tools: Optional[List[Tools]] = None

    @field_validator("organization")
    def organization_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("organization cannot be empty")
        return v.strip() if v else v

    @field_validator("role")
    def role_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("role cannot be empty")
        return v.strip() if v else v

    @field_validator("end_date")
    def validate_end_date(cls, v, info: ValidationInfo):
        start_date = info.data.get("start_date")
        if v and start_date and v < start_date:
            raise ValueError("end_date cannot be before start_date")
        return v


class ReadVolunteering(BaseModel):
    id: UUID
    profile_id: UUID
    organization: str
    role: str
    cause: Cause
    start_date: date
    end_date: Optional[date]
    currently_volunteering: bool
    description: Optional[str]
    tools: Optional[List[Tools]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ReadVolunteeringWithRelations(ReadVolunteering):
    profile: Optional["ReadProfile"] = None

    class Config:
        from_attributes = True

from Entities.UserDTOs.profile_entity import ReadProfile
ReadVolunteeringWithRelations.model_rebuild()
