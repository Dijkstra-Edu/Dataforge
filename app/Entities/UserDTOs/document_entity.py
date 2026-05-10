from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, validator

# ----------------------
# Input DTOs
# ----------------------
class CreateDocument(BaseModel):
    username: str
    document_name: Optional[str] = None
    document_type: Optional[str] = None
    document_kind: Optional[str] = None
    latex: str
    base_structure: dict

    @validator('username')
    def username_cannot_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('username cannot be empty')
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
    username: str
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
