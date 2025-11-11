from typing import Optional, Annotated
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

class CreateLinks(BaseModel):
    user_id: UUID
    portfolio_link: Optional[str] = None
    github_user_name: Annotated[str, Field(min_length=1, strip_whitespace=True)]
    github_link: Optional[str] = None
    linkedin_user_name: Annotated[str, Field(min_length=1, strip_whitespace=True)]
    linkedin_link: Optional[str] = None
    leetcode_user_name: Annotated[str, Field(min_length=1, strip_whitespace=True)]
    leetcode_link: Optional[str] = None
    orcid_id: Optional[Annotated[str, Field(min_length=1, strip_whitespace=True)]] = None
    orcid_link: Optional[str] = None
    primary_email: Optional[str] = None
    secondary_email: Optional[str] = None
    school_email: Optional[str] = None
    work_email: Optional[str] = None

class UpdateLinks(BaseModel):
    portfolio_link: Optional[str] = None
    github_user_name: Optional[Annotated[str, Field(min_length=1, strip_whitespace=True)]] = None
    github_link: Optional[str] = None
    linkedin_user_name: Optional[Annotated[str, Field(min_length=1, strip_whitespace=True)]] = None
    linkedin_link: Optional[str] = None
    leetcode_user_name: Optional[Annotated[str, Field(min_length=1, strip_whitespace=True)]] = None
    leetcode_link: Optional[str] = None
    orcid_id: Optional[Annotated[str, Field(min_length=1, strip_whitespace=True)]] = None
    orcid_link: Optional[str] = None
    primary_email: Optional[str] = None
    secondary_email: Optional[str] = None
    school_email: Optional[str] = None
    work_email: Optional[str] = None

class ReadLinks(BaseModel):
    id: UUID
    user_id: UUID
    portfolio_link: Optional[str]
    github_user_name: str
    github_link: Optional[str]
    linkedin_user_name: str
    linkedin_link: Optional[str]
    leetcode_user_name: str
    leetcode_link: Optional[str]
    orcid_id: Optional[str]
    orcid_link: Optional[str]
    primary_email: Optional[str]
    secondary_email: Optional[str]
    school_email: Optional[str]
    work_email: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
