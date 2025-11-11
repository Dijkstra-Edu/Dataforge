from typing import Optional, List, Annotated
from uuid import UUID
from datetime import datetime, date
from pydantic import BaseModel, Field
from Schema.SQL.Enums.enums import (CertificationType, Tools)


class CreateCertification(BaseModel):
    profile_id: UUID
    name: Annotated[str, Field(min_length=1, strip_whitespace=True)]
    type: CertificationType
    issuing_organization: Annotated[str, Field(min_length=1, strip_whitespace=True)]
    issue_date: date
    expiry_date: Optional[date] = None
    credential_id: Annotated[str, Field(min_length=1, strip_whitespace=True)]
    credential_url: Annotated[str, Field(min_length=1, strip_whitespace=True)]
    tools: Optional[List[Tools]] = None
    issuing_organization_logo: Optional[str] = None
    

class UpdateCertification(BaseModel):
    profile_id: Optional[UUID] = None
    name: Optional[Annotated[str, Field(min_length=1, strip_whitespace=True)]] = None
    type: Optional[CertificationType] = None
    issuing_organization: Optional[Annotated[str, Field(min_length=1, strip_whitespace=True)]] = None
    issue_date: Optional[date] = None
    expiry_date: Optional[date] = None
    credential_id: Optional[Annotated[str, Field(min_length=1, strip_whitespace=True)]] = None
    credential_url: Optional[Annotated[str, Field(min_length=1, strip_whitespace=True)]] = None
    tools: Optional[List[Tools]] = None
    issuing_organization_logo: Optional[str] = None
    
    
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
        