from uuid import UUID
from sqlmodel import Session
from typing import List, Optional
from datetime import date

from Schema.SQL.Models.models import WorkExperience, Profile, Location
from Schema.SQL.Enums.enums import EmploymentType, WorkLocationType, Domain, Tools
from Repository.User.workexperience_repository import WorkExperienceRepository
from Entities.UserDTOs.workexperience_entity import CreateWorkExperience, UpdateWorkExperience
from Utils.Exceptions.user_exceptions import LocationNotFound, ProfileNotFound, WorkExperienceNotFound

class WorkExperienceService:
    def __init__(self, session: Session):
        self.repo = WorkExperienceRepository(session)
        self.session = session

    def create_work_experience(self, work_experience_create: CreateWorkExperience) -> WorkExperience:
        # Check if profile exists
        profile = self.session.get(Profile, work_experience_create.profile_id)
        if not profile:
            raise ProfileNotFound(work_experience_create.profile_id)
        
        # Check if location exists if provided
        if work_experience_create.location:
            location = self.session.get(Location, work_experience_create.location)
            if not location:
                raise LocationNotFound(work_experience_create.location)
        
        work_experience = WorkExperience(**work_experience_create.dict(exclude_unset=True))
        return self.repo.create(work_experience)

    def get_work_experience(self, work_experience_id: UUID) -> Optional[WorkExperience]:
        work_experience = self.repo.get(work_experience_id)
        if not work_experience:
            raise WorkExperienceNotFound(work_experience_id)
        return work_experience

    def get_work_experiences_by_profile_id(self, profile_id: UUID) -> List[WorkExperience]:
        work_experiences = self.repo.get_by_profile_id(profile_id)
        if not work_experiences:
            raise WorkExperienceNotFound(profile_id)
        return work_experiences

    def list_work_experiences(
        self,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        order: str = "desc",
        profile_id: Optional[UUID] = None,
        title: Optional[str] = None,
        company_name: Optional[str] = None,
        employment_type: Optional[EmploymentType] = None,
        domain: Optional[List[Domain]] = None,
        location: Optional[UUID] = None,
        location_type: Optional[WorkLocationType] = None,
        currently_working: Optional[bool] = None,
        start_year_after: Optional[int] = None,
        start_year_before: Optional[int] = None,
    ) -> List[WorkExperience]:
        """
        Supports pagination, filtering, and sorting.
        """
        return self.repo.list(
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            order=order,
            profile_id=profile_id,
            title=title,
            company_name=company_name,
            employment_type=employment_type,
            domain=domain,
            location=location,
            location_type=location_type,
            currently_working=currently_working,
            start_year_after=start_year_after,
            start_year_before=start_year_before,
        )

    def autocomplete_work_experiences(
        self,
        query: str,
        field: str = "title",
        limit: int = 10,
    ) -> List[WorkExperience]:
        """
        Returns work experiences where the given field starts with or contains query text.
        """
        return self.repo.autocomplete(query=query, field=field, limit=limit)

    def update_work_experience(self, work_experience_id: UUID, work_experience_update: UpdateWorkExperience) -> Optional[WorkExperience]:
        work_experience = self.repo.get(work_experience_id)
        if not work_experience:
            return None
        
        # Check if profile is being updated and if it exists
        if work_experience_update.profile_id and work_experience_update.profile_id != work_experience.profile_id:
            profile = self.session.get(Profile, work_experience_update.profile_id)
            if not profile:
                raise ProfileNotFound(work_experience_update.profile_id)

        # Check if location is being updated and if it exists
        if work_experience_update.location and work_experience_update.location != work_experience.location:
            location = self.session.get(Location, work_experience_update.location)
            if not location:
                raise LocationNotFound(work_experience_update.location)
        
        update_data = work_experience_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(work_experience, key, value)
        return self.repo.update(work_experience)

    def delete_work_experience(self, work_experience_id: UUID) -> Optional[str]:
        work_experience = self.repo.get(work_experience_id)
        if not work_experience:
            raise WorkExperienceNotFound(work_experience_id)
        self.repo.delete(work_experience)
        return f"Work Experience {work_experience_id} deleted successfully"