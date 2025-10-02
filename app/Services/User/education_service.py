from uuid import UUID
from typing import List, Optional
from sqlmodel import Session

from Repository.User.education_repository import EducationRepository
from Entities.UserDTOs.education_entity import CreateEducation, UpdateEducation
from Schema.SQL.Models.models import Education
from Utils.Exceptions.user_exceptions import (
    EducationNotFound,
    ProfileNotFound,
    LocationNotFound,
)


class EducationService:
    def __init__(self, session: Session):
        self.repo = EducationRepository(session)
        self.session = session

    def create_education(self, education_create: CreateEducation) -> Education:
        # Verify Profile exists
        from Schema.SQL.Models.models import Profile, Location

        profile = self.session.get(Profile, education_create.profile_id)
        if not profile:
            raise ProfileNotFound(education_create.profile_id)

        location = self.session.get(Location, education_create.location)
        if not location:
            raise LocationNotFound(education_create.location)

        education = Education(**education_create.dict(exclude_unset=True))
        return self.repo.create(education)

    def get_education(self, education_id: UUID) -> Education:
        education = self.repo.get(education_id)
        if not education:
            raise EducationNotFound(education_id)
        return education

    def list_educations(
        self, skip: int = 0, limit: int = 20, profile_id: Optional[UUID] = None
    ) -> List[Education]:
        return self.repo.list(skip=skip, limit=limit, profile_id=profile_id)

    def update_education(
        self, education_id: UUID, education_update: UpdateEducation
    ) -> Education:
        education = self.repo.get(education_id)
        if not education:
            raise EducationNotFound(education_id)

        update_data = education_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(education, key, value)

        return self.repo.update(education)

    def delete_education(self, education_id: UUID) -> str:
        education = self.repo.get(education_id)
        if not education:
            raise EducationNotFound(education_id)
        self.repo.delete(education)
        return f"Education {education_id} deleted successfully"
