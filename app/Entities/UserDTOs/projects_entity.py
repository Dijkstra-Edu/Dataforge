from typing import Optional, List, Annotated
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field
from Schema.SQL.Enums.enums import Domain, Tools

class CreateProject(BaseModel):
    profile_id: UUID
    name: Annotated[str, Field(min_length=1, strip_whitespace=True)]
    organization: Optional[str] = None
    owner: Annotated[str, Field(min_length=1, strip_whitespace=True)]
    private: bool
    github_stars: Annotated[int, Field(ge=0)] = 0
    github_about: Optional[str] = None
    github_open_issues: Annotated[int, Field(ge=0)] = 0
    github_forks: Annotated[int, Field(ge=0)] = 0
    description: Annotated[str, Field(min_length=1, strip_whitespace=True)]
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
    total_lines_contributed: Optional[Annotated[int, Field(ge=0)]] = 0
    improper_uploads: Optional[bool] = False
    complexity_rating: Optional[float] = None
    testing_framework_present: bool
    testing_framework: Optional[str] = None
    project_organization_logo: Optional[str] = None


class UpdateProject(BaseModel):
    profile_id: Optional[UUID] = None
    name: Optional[Annotated[str, Field(min_length=1, strip_whitespace=True)]] = None
    organization: Optional[str] = None
    owner: Optional[Annotated[str, Field(min_length=1, strip_whitespace=True)]] = None
    private: Optional[bool] = None
    github_stars: Optional[Annotated[int, Field(ge=0)]] = None
    github_about: Optional[str] = None
    github_open_issues: Optional[Annotated[int, Field(ge=0)]] = None
    github_forks: Optional[Annotated[int, Field(ge=0)]] = None
    description: Optional[Annotated[str, Field(min_length=1, strip_whitespace=True)]] = None
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
