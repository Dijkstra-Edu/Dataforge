from typing import Optional, List, Dict, TYPE_CHECKING
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, validator

if TYPE_CHECKING:
    from Entities.UserDTOs.user_entity import ReadUser
    from Entities.UserDTOs.education_entity import ReadEducationWithLocation
    from Entities.UserDTOs.workexperience_entity import ReadWorkExperienceWithLocation
    from Entities.UserDTOs.certification_entity import ReadCertification
    from Entities.UserDTOs.publication_entity import ReadPublication
    from Entities.UserDTOs.volunteering_entity import ReadVolunteering
    from Entities.UserDTOs.projects_entity import ReadProject

# ----------------------
# Input DTOs
# ----------------------
class CreateProfile(BaseModel):
    user_id: UUID

    @validator('user_id')
    def user_id_must_be_valid_uuid(cls, v):
        if not v:
            raise ValueError('user_id cannot be empty')
        return v


class UpdateProfile(BaseModel):
    user_id: Optional[UUID] = None

    @validator('user_id')
    def user_id_must_be_valid_uuid(cls, v):
        if v is not None and not v:
            raise ValueError('user_id cannot be empty')
        return v


# ----------------------
# Output DTO
# ----------------------
class ReadProfile(BaseModel):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ----------------------
# Extended Output DTO with User details
# ----------------------
class ReadProfileWithUser(ReadProfile):
    user: Optional['ReadUser'] = None

    class Config:
        from_attributes = True


# ----------------------
# Extended Output DTO with full nested data
# ----------------------
class ReadProfileFull(ReadProfile):
    education: List['ReadEducationWithLocation'] = []
    work_experience: List['ReadWorkExperienceWithLocation'] = []
    certifications: List['ReadCertification'] = []
    publications: List['ReadPublication'] = []
    volunteering: List['ReadVolunteering'] = []
    projects: List['ReadProject'] = []
    leetcode: Optional[Dict] = None  # Excluded for now
    
    class Config:
        from_attributes = True

