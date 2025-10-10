from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, field_validator

class CreateLinks(BaseModel):
    user_id: UUID
    portfolio_link: Optional[str] = None
    github_user_name: str
    github_link: Optional[str] = None
    linkedin_user_name: str
    linkedin_link: Optional[str] = None
    leetcode_user_name: str
    leetcode_link: Optional[str] = None
    orcid_id: Optional[str] = None
    orcid_link: Optional[str] = None

    @field_validator("github_user_name", "linkedin_user_name", "leetcode_user_name")
    def validate_not_empty(cls, v: str):
        if not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()
    
    @field_validator("orcid_id")
    def validate_orcid_not_empty(cls, v: Optional[str]):
        if v is not None and not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip() if v else v

class UpdateLinks(BaseModel):
    portfolio_link: Optional[str] = None
    github_user_name: Optional[str] = None
    github_link: Optional[str] = None
    linkedin_user_name: Optional[str] = None
    linkedin_link: Optional[str] = None
    leetcode_user_name: Optional[str] = None
    leetcode_link: Optional[str] = None
    orcid_id: Optional[str] = None
    orcid_link: Optional[str] = None

    @field_validator("github_user_name", "linkedin_user_name", "leetcode_user_name", "orcid_id")
    def validate_not_empty_if_present(cls, v: Optional[str]):
        if v is not None and not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip() if v else v

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
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
