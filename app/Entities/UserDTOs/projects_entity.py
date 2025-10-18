from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from Schema.SQL.Enums.enums import Domain, Tools

class CreateProject(BaseModel):
    profile_id: UUID
    name: str = Field(..., min_length=1)
    organization: Optional[str] = None
    owner: str = Field(..., min_length=1)  
    private: bool
    github_stars: int = 0
    github_about: Optional[str] = None
    github_open_issues: int = 0
    github_forks: int = 0
    description: str = Field(..., min_length=1)
    domain: Domain
    topics: Optional[List[str]] = None
    tools: List[Tools]
    readme: bool
    license: bool
    landing_page: bool
    landing_page_link: Optional[str] = None
    docs_page: bool
    docs_page_link: Optional[str] = None
    own_domain_name: bool
    domain_name: Optional[str] = None
    total_lines_contributed: Optional[int] = 0
    improper_uploads: Optional[bool] = False
    complexity_rating: Optional[float] = None
    testing_framework_present: bool
    testing_framework: Optional[str] = None
    project_organization_logo: Optional[str] = None

    @field_validator("name", "owner", "description")
    def must_not_be_empty(cls, v, info):
        if not v.strip():
            raise ValueError(f"{info.field_name} cannot be empty")
        return v.strip()

    @field_validator("github_stars", "github_open_issues", "github_forks", "total_lines_contributed")
    def must_be_non_negative(cls, v, info):
        if v is not None and v < 0:
            raise ValueError(f"{info.field_name} cannot be negative")
        return v


class UpdateProject(BaseModel):
    profile_id: Optional[UUID] = None
    name: Optional[str] = None
    organization: Optional[str] = None
    owner: Optional[str] = None
    private: Optional[bool] = None
    github_stars: Optional[int] = None
    github_about: Optional[str] = None
    github_open_issues: Optional[int] = None
    github_forks: Optional[int] = None
    description: Optional[str] = None
    domain: Optional[Domain] = None
    topics: Optional[List[str]] = None
    tools: Optional[List[Tools]] = None
    readme: Optional[bool] = None
    license: Optional[bool] = None
    landing_page: Optional[bool] = None
    landing_page_link: Optional[str] = None
    docs_page: Optional[bool] = None
    docs_page_link: Optional[str] = None
    own_domain_name: Optional[bool] = None
    domain_name: Optional[str] = None
    total_lines_contributed: Optional[int] = None
    improper_uploads: Optional[bool] = None
    complexity_rating: Optional[float] = None
    testing_framework_present: Optional[bool] = None
    testing_framework: Optional[str] = None
    project_organization_logo: Optional[str] = None

    @field_validator("name", "owner", "description")
    def must_not_be_empty_if_provided(cls, v, info):
        if v is not None and not v.strip():
            raise ValueError(f"{info.field_name} cannot be empty")
        return v.strip() if v else v

    @field_validator("github_stars", "github_open_issues", "github_forks")
    def must_be_non_negative(cls, v, info):
        if v is not None and v < 0:
            raise ValueError(f"{info.field_name} cannot be negative")
        return v

class ReadProject(BaseModel):
    id: UUID
    profile_id: UUID
    name: str
    organization: Optional[str]
    owner: str
    private: bool
    github_stars: int
    github_about: Optional[str]
    github_open_issues: int
    github_forks: int
    description: str
    domain: Domain
    topics: Optional[List[str]]
    tools: List[Tools]
    readme: bool
    license: bool
    landing_page: bool
    landing_page_link: Optional[str]
    docs_page: bool
    docs_page_link: Optional[str]
    own_domain_name: bool
    domain_name: Optional[str]
    total_lines_contributed: Optional[int]
    improper_uploads: Optional[bool]
    complexity_rating: Optional[float]
    testing_framework_present: bool
    testing_framework: Optional[str]
    project_organization_logo: Optional[str]
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
