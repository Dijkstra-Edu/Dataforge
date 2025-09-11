# schemas/organizations_schema.py
from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class CreateOrganization(BaseModel):
    name: str
    image: Optional[str] = None
    repo_link: Optional[str] = None

class UpdateOrganization(BaseModel):
    name: Optional[str] = None
    image: Optional[str] = None
    repo_link: Optional[str] = None

class ReadOrganization(BaseModel):
    id: UUID
    name: Optional[str]
    image: Optional[str]
    repo_link: Optional[str]
    created_at: datetime
    updated_at: datetime
