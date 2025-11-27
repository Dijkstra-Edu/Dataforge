from typing import Optional
from uuid import UUID
from datetime import datetime, date
from pydantic import BaseModel, field_validator
from Schema.SQL.Enums.enums import TestScoreType

class CreateTestScore(BaseModel):
    profile_id: UUID
    title: str
    type: TestScoreType
    score: str
    test_date: date
    description: Optional[str] = None
    
    @field_validator('title')
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty.")
        return v.strip()
    
    @field_validator('score')
    def score_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Score cannot be empty.")
        return v.strip()
    
    @field_validator('test_date')
    def test_date_must_not_be_empty(cls, v):
        if v is None:
            raise ValueError("Test Date cannot be empty.")
        return v

class UpdateTestScore(BaseModel):
    profile_id: Optional[UUID] = None
    title: Optional[str] = None
    type: Optional[TestScoreType] = None
    score: Optional[str] = None
    test_date: Optional[date] = None
    description: Optional[str] = None
    
    @field_validator('title')
    def title_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty.")
        return v.strip() if v else v
    
    @field_validator('score')
    def score_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Score cannot be empty.")
        return v.strip() if v else v

class ReadTestScore(BaseModel):
    id: UUID
    profile_id: UUID
    title: str
    type: TestScoreType
    score: str
    test_date: date
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
