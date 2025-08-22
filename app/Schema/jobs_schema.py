# schemas/jobs_schema.py
from typing import Optional, List
from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel

class JobCreate(BaseModel):
    title: str
    department: Optional[str] = None
    company_name: Optional[str] = None
    organization: UUID

class JobUpdate(BaseModel):
    title: Optional[str] = None
    department: Optional[str] = None
    company_name: Optional[str] = None

class JobRead(BaseModel):
    id: UUID
    title: Optional[str]
    department: Optional[str]
    company_name: Optional[str]
    organization: UUID
    created_at: datetime
    updated_at: datetime
