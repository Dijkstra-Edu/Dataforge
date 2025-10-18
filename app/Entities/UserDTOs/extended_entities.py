"""
Extended DTOs with circular dependencies.
This module imports from multiple entity files and defines models that reference each other.
"""
from __future__ import annotations

from typing import Optional, List, Dict

# Import all the basic DTOs
from Entities.UserDTOs.profile_entity import ReadProfile
from Entities.UserDTOs.user_entity import ReadUser
from Entities.UserDTOs.links_entity import ReadLinks
from Entities.UserDTOs.education_entity import ReadEducationWithLocation
from Entities.UserDTOs.workexperience_entity import ReadWorkExperienceWithLocation
from Entities.UserDTOs.certification_entity import ReadCertification
from Entities.UserDTOs.publication_entity import ReadPublication
from Entities.UserDTOs.volunteering_entity import ReadVolunteering
from Entities.UserDTOs.projects_entity import ReadProject


# ----------------------
# Extended Profile DTOs
# ----------------------
class ReadProfileWithUser(ReadProfile):
    """Profile with user details"""
    user: Optional[ReadUser] = None

    class Config:
        from_attributes = True


class ReadProfileFull(ReadProfile):
    """Profile with all nested relationships"""
    education: List[ReadEducationWithLocation] = []
    work_experience: List[ReadWorkExperienceWithLocation] = []
    certifications: List[ReadCertification] = []
    publications: List[ReadPublication] = []
    volunteering: List[ReadVolunteering] = []
    projects: List[ReadProject] = []
    leetcode: Optional[Dict] = None  # Excluded for now
    
    class Config:
        from_attributes = True


# ----------------------
# Extended User DTOs
# ----------------------
class ReadUserFull(ReadUser):
    """User with links and full profile data"""
    links: Optional[ReadLinks] = None
    profile: Optional[ReadProfileFull] = None
    
    class Config:
        from_attributes = True

