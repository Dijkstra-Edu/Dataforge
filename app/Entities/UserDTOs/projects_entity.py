from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from Schema.SQL.Enums.enums import Domain, Tools

class CreateProject(BaseModel):
    username: str
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    github_repo_url: str
    domain: Domain
    topics: Optional[List[str]] = None
    tools: List[Tools]
    landing_page_link: Optional[str] = None
    docs_page_link: Optional[str] = None

    @field_validator("name",  "description")
    def must_not_be_empty(cls, v, info):
        if not v.strip():
            raise ValueError(f"{info.field_name} cannot be empty")
        return v.strip()

class UpdateProject(BaseModel):
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    github_repo_url: str
    domain: Domain
    topics: Optional[List[str]] = None
    tools: List[Tools]
    landing_page_link: Optional[str] = None
    docs_page_link: Optional[str] = None

    @field_validator("name",  "description")
    def must_not_be_empty(cls, v, info):
        if not v.strip():
            raise ValueError(f"{info.field_name} cannot be empty")
        return v.strip()

class ReadProject(BaseModel):
    id: UUID
    username: str
    profile_id: UUID

    name: str

    github_repo_url: Optional[str]
    github_stars: Optional[int] = None
    github_about: Optional[str] = None
    github_open_issues: Optional[int] = None
    github_forks: Optional[int] = None

    description: str
    domain: Domain
    topics: Optional[List[str]] = None
    tools: Optional[List[Tools]] = None

    landing_page_link: Optional[str] = None
    docs_page_link: Optional[str] = None
    domain_name: Optional[str] = None

    total_lines_contributed: Optional[int] = None
    repo_analysis: Optional[dict] = None

    project_organization_logo: Optional[str] = None

    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True  

class DeleteResponse(BaseModel):
    detail: str

class ReadProjectWithRelations(ReadProject):
    profile: Optional["ReadProfile"] = None

    class Config:
        from_attributes = True


from Entities.UserDTOs.profile_entity import ReadProfile
ReadProjectWithRelations.model_rebuild()
