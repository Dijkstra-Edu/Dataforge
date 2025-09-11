from typing import Optional, List
from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel

from Entities.SQL.Enums.enums import Tools


# Input DTOs
class CreateFellowship(BaseModel):
    title: str
    organization: UUID
    hero_image: Optional[str] = None
    location: Optional[str] = None
    location_type: Optional[str] = None
    duration_weeks: Optional[int] = None
    stipend_month: Optional[float] = None
    stipend_currency: Optional[str] = None
    application_deadline: Optional[date] = None
    start_date: Optional[date] = None
    description: Optional[str] = None
    featured: Optional[bool] = None
    highlight: Optional[str] = None
    category: Optional[str] = None
    benefits: Optional[List[str]] = []
    requirements: Optional[List[str]] = []
    technologies: Optional[List[Tools]] = []


class UpdateFellowship(BaseModel):
    title: Optional[str] = None
    organization: Optional[UUID] = None
    hero_image: Optional[str] = None
    location: Optional[str] = None
    location_type: Optional[str] = None
    duration_weeks: Optional[int] = None
    stipend_month: Optional[float] = None
    stipend_currency: Optional[str] = None
    application_deadline: Optional[date] = None
    start_date: Optional[date] = None
    description: Optional[str] = None
    featured: Optional[bool] = None
    highlight: Optional[str] = None
    category: Optional[str] = None
    benefits: Optional[List[str]] = None
    requirements: Optional[List[str]] = None
    technologies: Optional[List[Tools]] = None


# Output DTO
class ReadFellowship(BaseModel):
    id: UUID
    title: Optional[str]
    organization: UUID
    hero_image: Optional[str]
    location: Optional[str]
    location_type: Optional[str]
    duration_weeks: Optional[int]
    stipend_month: Optional[float]
    stipend_currency: Optional[str]
    application_deadline: Optional[date]
    start_date: Optional[date]
    description: Optional[str]
    featured: Optional[bool]
    highlight: Optional[str]
    category: Optional[str]
    benefits: Optional[List[str]]
    requirements: Optional[List[str]]
    technologies: Optional[List[Tools]]
    created_at: datetime
    updated_at: datetime
