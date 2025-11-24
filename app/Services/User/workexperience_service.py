from uuid import UUID
from sqlmodel import Session
from typing import List, Optional
from datetime import date

from Schema.SQL.Models.models import WorkExperience, Profile, Location
from Schema.SQL.Enums.enums import EmploymentType, WorkLocationType, Domain, Tools
from Repository.User.workexperience_repository import WorkExperienceRepository
from Repository.User.location_repository import LocationRepository
from Entities.UserDTOs.workexperience_entity import CreateWorkExperience, UpdateWorkExperience, ReadWorkExperience
from Entities.UserDTOs.location_entity import CreateLocation, ReadLocation
from Utils.Exceptions.user_exceptions import LocationNotFound, ProfileNotFound, WorkExperienceNotFound

class WorkExperienceService:
    def __init__(self, session: Session):
        self.repo = WorkExperienceRepository(session)
        self.location_repo = LocationRepository(session)
        self.session = session

    def _convert_to_read_dto(self, work_experience: WorkExperience) -> ReadWorkExperience:
        """Convert WorkExperience database model to ReadWorkExperience DTO with populated location"""
        work_exp_dict = work_experience.dict()
        
        # Populate location data if location_id exists
        if work_experience.location:
            try:
                location = self.location_repo.get(work_experience.location)
                if location:
                    work_exp_dict['location'] = ReadLocation.model_validate(location).model_dump()
                else:
                    work_exp_dict['location'] = None
            except:
                work_exp_dict['location'] = None
        else:
            work_exp_dict['location'] = None
        
        return ReadWorkExperience.model_validate(work_exp_dict)

    def _convert_list_to_read_dto(self, work_experiences: List[WorkExperience]) -> List[ReadWorkExperience]:
        """Convert list of WorkExperience database models to ReadWorkExperience DTOs with populated locations"""
        return [self._convert_to_read_dto(we) for we in work_experiences]

    def create_work_experience(self, work_experience_create: CreateWorkExperience) -> ReadWorkExperience:
        # Check if profile exists
        profile = self.session.get(Profile, work_experience_create.profile_id)
        if not profile:
            raise ProfileNotFound(work_experience_create.profile_id)
        
        # Handle location creation if provided
        location_id = None
        if work_experience_create.location:
            location_data = work_experience_create.location
            
            # Check if location has an ID - if yes, use existing location
            if location_data.id:
                # Verify the existing location exists
                existing_location = self.location_repo.get(location_data.id)
                if existing_location:
                    location_id = location_data.id
                else:
                    # Location ID provided but doesn't exist - create new location
                    location = Location(**location_data.dict(exclude_unset=True, exclude={'id'}))
                    created_location = self.location_repo.create(location)
                    location_id = created_location.id
            else:
                # No ID provided - create new location
                location = Location(**location_data.dict(exclude_unset=True, exclude={'id'}))
                created_location = self.location_repo.create(location)
                location_id = created_location.id
        
        # Create work experience data excluding the location object
        work_experience_data = work_experience_create.dict(exclude_unset=True, exclude={'location'})
        work_experience_data['location'] = location_id
        
        work_experience = WorkExperience(**work_experience_data)
        created_work_experience = self.repo.create(work_experience)
        return self._convert_to_read_dto(created_work_experience)

    def get_work_experience(self, work_experience_id: UUID) -> Optional[ReadWorkExperience]:
        work_experience = self.repo.get(work_experience_id)
        if not work_experience:
            raise WorkExperienceNotFound(work_experience_id)
        return self._convert_to_read_dto(work_experience)

    def get_work_experiences_by_profile_id(self, profile_id: UUID) -> List[ReadWorkExperience]:
        work_experiences = self.repo.get_by_profile_id(profile_id)
        return self._convert_list_to_read_dto(work_experiences)

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
    ) -> List[ReadWorkExperience]:
        """
        Supports pagination, filtering, and sorting.
        """
        work_experiences = self.repo.list(
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
        return self._convert_list_to_read_dto(work_experiences)

    def autocomplete_work_experiences(
        self,
        query: str,
        field: str = "title",
        limit: int = 10,
    ) -> List[ReadWorkExperience]:
        """
        Returns work experiences where the given field starts with or contains query text.
        """
        work_experiences = self.repo.autocomplete(query=query, field=field, limit=limit)
        return self._convert_list_to_read_dto(work_experiences)

    def update_work_experience(self, work_experience_id: UUID, work_experience_update: UpdateWorkExperience) -> Optional[ReadWorkExperience]:
        work_experience = self.repo.get(work_experience_id)
        if not work_experience:
            return None
        
        # Check if profile is being updated and if it exists
        if work_experience_update.profile_id and work_experience_update.profile_id != work_experience.profile_id:
            profile = self.session.get(Profile, work_experience_update.profile_id)
            if not profile:
                raise ProfileNotFound(work_experience_update.profile_id)

        # Handle location update if provided
        if work_experience_update.location is not None:
            if work_experience_update.location:
                location_data = work_experience_update.location
                
                # Check if location has an ID - if yes, update existing location
                if location_data.id:
                    # Update existing location
                    existing_location = self.location_repo.get(location_data.id)
                    if existing_location:
                        # Update the existing location with new data
                        update_data = location_data.dict(exclude_unset=True, exclude={'id'})
                        for key, value in update_data.items():
                            setattr(existing_location, key, value)
                        self.location_repo.update(existing_location)
                        work_experience.location = location_data.id
                    else:
                        # Location ID provided but doesn't exist - create new location
                        location = Location(**location_data.dict(exclude_unset=True, exclude={'id'}))
                        created_location = self.location_repo.create(location)
                        work_experience.location = created_location.id
                else:
                    # No ID provided - create new location
                    location = Location(**location_data.dict(exclude_unset=True, exclude={'id'}))
                    created_location = self.location_repo.create(location)
                    work_experience.location = created_location.id
            else:
                # Set location to None if explicitly provided as None
                work_experience.location = None
        
        # Update other fields
        update_data = work_experience_update.dict(exclude_unset=True, exclude={'location'})
        for key, value in update_data.items():
            setattr(work_experience, key, value)
        updated_work_experience = self.repo.update(work_experience)
        return self._convert_to_read_dto(updated_work_experience) if updated_work_experience else None

    def delete_work_experience(self, work_experience_id: UUID) -> Optional[str]:
        work_experience = self.repo.get(work_experience_id)
        if not work_experience:
            raise WorkExperienceNotFound(work_experience_id)
        self.repo.delete(work_experience)
        return f"Work Experience {work_experience_id} deleted successfully"

    def get_work_experiences_by_profile_with_locations(self, profile_id: UUID) -> List[ReadWorkExperience]:
        """
        Get all work experiences for a profile with their associated locations populated.
        Returns empty list if no work experiences found.
        """
        return self.get_work_experiences_by_profile_id(profile_id)

    def get_work_experiences_by_github_username(self, github_username: str) -> List[ReadWorkExperience]:
        """Get all work experiences by GitHub username"""
        from Services.User.profile_service import ProfileService
        
        profile_service = ProfileService(self.session)
        profile_id = profile_service.get_profile_id_by_github_username(github_username)
        return self.get_work_experiences_by_profile_id(profile_id)
    
    def get_work_experiences_by_github_username_with_locations(self, github_username: str) -> List[ReadWorkExperience]:
        """Get all work experiences with locations by GitHub username"""
        return self.get_work_experiences_by_github_username(github_username)