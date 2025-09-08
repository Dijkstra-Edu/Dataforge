# schemas/projects_opportunities_schema.py
from typing import List, Optional
from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel
from Entities.SQL.Enums.enums import ProjectLevel, Difficulty, Tools

class CreateProject(BaseModel):
    title: str
    project_level: Optional[ProjectLevel] = None
    is_user_project: Optional[bool] = None
    owner: Optional[str] = None
    organization: Optional[UUID] = None
    organization_logo: Optional[str] = None
    hero_image: Optional[str] = None
    repository: Optional[str] = None
    languages: Optional[List[Tools]] = []
    frameworks: Optional[List[Tools]] = []
    stars: Optional[int] = None
    forks: Optional[int] = None
    last_updated: Optional[date] = None
    description: Optional[str] = None
    featured: Optional[bool] = None
    highlight: Optional[str] = None
    category: Optional[List[str]] = []
    difficulty: Optional[Difficulty] = None
    issues_count: Optional[int] = None
    contributors_count: Optional[int] = None
    license: Optional[str] = None
    topics: Optional[List[str]] = []

class UpdateProject(BaseModel):
    title: Optional[str] = None
    project_level: Optional[ProjectLevel] = None
    is_user_project: Optional[bool] = None
    owner: Optional[str] = None
    organization: Optional[UUID] = None
    organization_logo: Optional[str] = None
    hero_image: Optional[str] = None
    repository: Optional[str] = None
    languages: Optional[List[Tools]] = []
    frameworks: Optional[List[Tools]] = []
    stars: Optional[int] = None
    forks: Optional[int] = None
    last_updated: Optional[date] = None
    description: Optional[str] = None
    featured: Optional[bool] = None
    highlight: Optional[str] = None
    category: Optional[List[str]] = []
    difficulty: Optional[Difficulty] = None
    issues_count: Optional[int] = None
    contributors_count: Optional[int] = None
    license: Optional[str] = None
    topics: Optional[List[str]] = []

class ReadProject(BaseModel):
    id: UUID
    title: Optional[str]
    project_level: Optional[ProjectLevel]
    is_user_project: Optional[bool]
    owner: Optional[str]
    organization: Optional[UUID]
    organization_logo: Optional[str]
    hero_image: Optional[str]
    repository: Optional[str]
    languages: Optional[List[Tools]]
    frameworks: Optional[List[Tools]]
    stars: Optional[int]
    forks: Optional[int]
    last_updated: Optional[date]
    description: Optional[str]
    featured: Optional[bool]
    highlight: Optional[str]
    category: Optional[List[str]]
    difficulty: Optional[Difficulty]
    issues_count: Optional[int]
    contributors_count: Optional[int]
    license: Optional[str]
    topics: Optional[List[str]]
    created_at: datetime
    updated_at: datetime
