from typing import Optional, List, Annotated
from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel, ValidationInfo, field_validator, Field
from Schema.SQL.Enums.enums import (
    Cause,
    Tools,
)  

class CreateVolunteering(BaseModel):
    profile_id: UUID
    organization: Annotated[str, Field(min_length=1, strip_whitespace=True)]
    role: Annotated[str, Field(min_length=1, strip_whitespace=True)]
    cause: Cause
    start_date: date
    end_date: Optional[date] = None
    currently_volunteering: bool
    description: Optional[str] = None
    tools: Optional[List[Tools]] = None
    organization_logo: Optional[str] = None

    @field_validator("end_date")
    def validate_end_date(cls, v, info: ValidationInfo):
        start_date = info.data.get("start_date")
        if v and start_date and v < start_date:
            raise ValueError("end_date cannot be before start_date")
        return v


class UpdateVolunteering(BaseModel):
    profile_id: Optional[UUID] = None
    organization: Optional[Annotated[str, Field(min_length=1, strip_whitespace=True)]] = None
    role: Optional[Annotated[str, Field(min_length=1, strip_whitespace=True)]] = None
    cause: Optional[Cause] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    currently_volunteering: Optional[bool] = None
    description: Optional[str] = None
    tools: Optional[List[Tools]] = None
    organization_logo: Optional[str] = None

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
    organization_logo: Optional[str]
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
