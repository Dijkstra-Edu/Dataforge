# schemas/jobs_schema.py
from typing import Optional, List
from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel

from Schema.SQL.Enums.enums import WorkLocationType, EmploymentType, Currency, Tools

# ----------------------
# Input DTOs
# ----------------------
class CreateJob(BaseModel):
    title: str
    department: Optional[str] = None
    company_name: Optional[str] = None
    company_logo: Optional[str] = None
    hero_image: Optional[str] = None
    location: Optional[str] = None
    location_type: Optional[WorkLocationType] = None
    employment_type: Optional[EmploymentType] = None
    experience_level: Optional[str] = None
    experience_yoe: Optional[float] = None
    posted_date: Optional[date] = None
    salary_annual_min: Optional[int] = None
    salary_annual_max: Optional[int] = None
    salary_currency: Optional[Currency] = None
    description: Optional[str] = None
    featured: Optional[bool] = None
    highlight: Optional[str] = None
    category: Optional[str] = None
    perks: Optional[List[str]] = []
    organization: UUID
    technologies: Optional[List[Tools]] = []


class UpdateJob(BaseModel):
    title: Optional[str] = None
    department: Optional[str] = None
    company_name: Optional[str] = None
    company_logo: Optional[str] = None
    hero_image: Optional[str] = None
    location: Optional[str] = None
    location_type: Optional[WorkLocationType] = None
    employment_type: Optional[EmploymentType] = None
    experience_level: Optional[str] = None
    experience_yoe: Optional[float] = None
    posted_date: Optional[date] = None
    salary_annual_min: Optional[int] = None
    salary_annual_max: Optional[int] = None
    salary_currency: Optional[Currency] = None
    description: Optional[str] = None
    featured: Optional[bool] = None
    highlight: Optional[str] = None
    category: Optional[str] = None
    perks: Optional[List[str]] = None
    organization: Optional[UUID] = None
    technologies: Optional[List[Tools]] = []


# ----------------------
# Output DTO
# ----------------------
class ReadJob(BaseModel):
    id: UUID
    title: Optional[str]
    department: Optional[str]
    company_name: Optional[str]
    company_logo: Optional[str]
    hero_image: Optional[str]
    location: Optional[str]
    location_type: Optional[WorkLocationType]
    employment_type: Optional[EmploymentType]
    experience_level: Optional[str]
    experience_yoe: Optional[float]
    posted_date: Optional[date]
    salary_annual_min: Optional[int]
    salary_annual_max: Optional[int]
    salary_currency: Optional[Currency]
    description: Optional[str]
    featured: Optional[bool]
    highlight: Optional[str]
    category: Optional[str]
    perks: Optional[List[str]]
    organization: UUID
    created_at: datetime
    updated_at: datetime
    technologies: Optional[List[Tools]] = []

    class Config:
        from_attributes = True

