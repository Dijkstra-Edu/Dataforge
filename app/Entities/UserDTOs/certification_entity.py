from typing import Optional,List
from uuid import UUID
from datetime import datetime, date
from pydantic import BaseModel, field_validator
from Schema.SQL.Enums.enums import (CertificationType, Tools)
class CreateCertification(BaseModel):
    profile_id: UUID
    name: str
    type: CertificationType
    issuing_organization: str
    issue_date: date
    expiry_date: Optional[date] = None
    credential_id: str
    credential_url:str
    tools:Optional[List[Tools]]
    issuing_organization_logo: Optional[str] = None
    
    @field_validator('name')
    def name_must_not_be_empty(cls ,v):
        if not v.strip():
            raise ValueError("Name cannot be empty.")
        return v.strip()
    
    @field_validator('issuing_organization')
    def issuing_organization_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Issuing Organization cannot be empty.")
        return v.strip()
    
    @field_validator('issue_date')
    def issue_date_must_not_be_empty(cls, v):
        if v is None:
            raise ValueError("Issue Date cannot be empty.")
        return v
    
    @field_validator('credential_id')
    def credential_id_must_not_be_empty(cls,v):
        if not v.strip():
            raise ValueError("Credential id cannot be empty.")
        return v.strip()
    
    @field_validator('credential_url')
    def credential_url_must_not_be_empty(cls,v):
        if not v.strip():
            raise ValueError("Credential url cannot be empty.")
        return v.strip()
    

class UpdateCertification(BaseModel):
    profile_id: Optional[UUID] = None
    name: Optional[str] = None
    type: Optional[CertificationType] = None
    issuing_organization: Optional[str] = None
    issue_date: Optional[date] = None
    expiry_date: Optional[date] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None
    tools: Optional[List[Tools]] = None
    issuing_organization_logo: Optional[str] = None
    
    @field_validator('name')
    def name_must_not_be_empty(cls ,v):
        if v is not None and not v.strip():
            raise ValueError("Name cannot be empty.")
        return v.strip() if v else v
    
    @field_validator('issuing_organization')
    def issuing_organization_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Issuing Organization cannot be empty.")
        return v.strip() if v else v
    
    @field_validator('issue_date')
    def issue_date_must_not_be_empty(cls, v):
        # For optional updates, v can be None, which is valid
        # If v is provided, it should be a valid date (validated by pydantic automatically)
        return v
    
    @field_validator('credential_id')
    def credential_id_must_not_be_empty(cls,v):
        if v is not None and not v.strip():
            raise ValueError("Credential id cannot be empty.")
        return v.strip() if v else v
    
    @field_validator('credential_url')
    def credential_url_must_not_be_empty(cls,v):
        if v is not None and not v.strip():
            raise ValueError("Credential url cannot be empty.")
        return v.strip() if v else v
    
    
class ReadCertification(BaseModel):
    id: UUID
    profile_id: UUID
    name: str
    type: CertificationType
    issuing_organization: str
    issue_date: date
    expiry_date: Optional[date] = None
    credential_id: str
    credential_url:str
    tools:Optional[List[Tools]]
    issuing_organization_logo: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        