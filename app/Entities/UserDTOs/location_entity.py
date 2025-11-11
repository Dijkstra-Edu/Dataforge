from typing import Optional, Annotated
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

class CreateLocation(BaseModel):
    id: Optional[UUID] = None
    city: str
    state: Optional[str] = None
    country: Annotated[str, Field(min_length=1, strip_whitespace=True)]
    longitude: Optional[float] = None
    latitude: Optional[float] = None

class UpdateLocation(BaseModel):
    city: Optional[Annotated[str, Field(min_length=1, strip_whitespace=True)]] = None
    state: Optional[str] = None
    country: Optional[Annotated[str, Field(min_length=1, strip_whitespace=True)]] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None

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