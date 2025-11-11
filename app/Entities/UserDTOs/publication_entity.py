from typing import Optional, List
from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel, field_validator

from Schema.SQL.Enums.enums import Tools  

class CreatePublication(BaseModel):
    profile_id: UUID
    title: str
    publisher: str
    authors: List[str]
    publication_date: date
    publication_url: str
    description: str
    tools: Optional[List[Tools]] = None
    publisher_logo: Optional[str] = None

    @field_validator("title")
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("title cannot be empty")
        return v.strip()

    @field_validator("publisher")
    def publisher_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("publisher cannot be empty")
        return v.strip()

    @field_validator("authors")
    def authors_must_not_be_empty(cls, v):
        if not v or len(v) == 0:
            raise ValueError("authors cannot be empty")
        return v

    @field_validator("publication_url")
    def url_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("publication_url cannot be empty")
        return v.strip()

    @field_validator("description")
    def description_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("description cannot be empty")
        return v.strip()


class UpdatePublication(BaseModel):
    profile_id: Optional[UUID] = None
    title: Optional[Annotated[str, Field(min_length=1, strip_whitespace=True)]] = None
    publisher: Optional[Annotated[str, Field(min_length=1, strip_whitespace=True)]] = None
    authors: Optional[List[Annotated[str, Field(min_length=1, strip_whitespace=True)]]] = None
    publication_date: Optional[date] = None
    publication_url: Optional[Annotated[str, Field(min_length=1, strip_whitespace=True)]] = None
    description: Optional[Annotated[str, Field(min_length=1, strip_whitespace=True)]] = None
    tools: Optional[List[Tools]] = None
    publisher_logo: Optional[str] = None


class ReadPublication(BaseModel):
    id: UUID
    profile_id: UUID
    title: str
    publisher: str
    authors: List[str]
    publication_date: date
    publication_url: str
    description: str
    tools: Optional[List[Tools]]
    publisher_logo: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ReadPublicationWithRelations(ReadPublication):
    profile: Optional["ReadProfile"] = None

    class Config:
        from_attributes = True


from Entities.UserDTOs.profile_entity import ReadProfile
ReadPublicationWithRelations.model_rebuild()
