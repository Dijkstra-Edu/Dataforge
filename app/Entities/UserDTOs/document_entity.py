from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, validator

# ----------------------
# Input DTOs
# ----------------------
class CreateDocument(BaseModel):
    github_username: str
    document_name: Optional[str] = None
    # 'row' or 'deedy'
    document_type: Optional[str] = None
    # 'resume' or 'cv'
    document_kind: Optional[str] = None
    latex: str
    base_structure: dict

    @validator('github_username')
    def github_username_cannot_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('github_username cannot be empty')
        return v.strip()

    class Config:
        from_attributes = True


class UpdateDocument(BaseModel):
    document_name: Optional[str] = None
    document_type: Optional[str] = None
    document_kind: Optional[str] = None
    latex: Optional[str] = None
    base_structure: Optional[dict] = None
    
    class Config:
        from_attributes = True


class ReadDocument(BaseModel):
    id: UUID
    profile_id: UUID
    document_name: Optional[str] = None
    document_type: Optional[str] = None
    document_kind: Optional[str] = None
    latex: Optional[str] = None
    base_structure: Optional[dict] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
