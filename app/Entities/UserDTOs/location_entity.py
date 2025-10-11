from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, field_validator

class CreateLocation(BaseModel):
    city: str
    state: Optional[str] = None
    country: str
    longitude: Optional[float] = None
    latitude: Optional[float] = None

    @field_validator('city')
    def city_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('city cannot be empty')
        return v.strip()

    @field_validator('country')
    def country_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('country cannot be empty')
        return v.strip()

class UpdateLocation(BaseModel):
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None

    @field_validator('city')
    def city_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('city cannot be empty')
        return v.strip() if v else v

    @field_validator('country')
    def country_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('country cannot be empty')
        return v.strip() if v else v

class ReadLocation(BaseModel):
    id: UUID
    city: str
    state: Optional[str]
    country: str
    longitude: Optional[float]
    latitude: Optional[float]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True