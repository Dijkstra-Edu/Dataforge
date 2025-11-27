from uuid import UUID
from typing import List, Optional
from sqlmodel import Session

from Repository.User.education_repository import EducationRepository
from Repository.User.location_repository import LocationRepository
from Entities.UserDTOs.education_entity import CreateEducation, UpdateEducation, ReadEducation
from Entities.UserDTOs.location_entity import CreateLocation, ReadLocation
from Schema.SQL.Models.models import Education, Profile, Location
from Utils.Exceptions.user_exceptions import EducationNotFound, ProfileNotFound, LocationNotFound


class EducationService:
    def __init__(self, session: Session):
        self.repo = EducationRepository(session)
        self.location_repo = LocationRepository(session)
        self.session = session

    def _convert_to_read_dto(self, education: Education) -> ReadEducation:
        """Convert Education database model to ReadEducation DTO with populated location"""
        education_dict = education.dict()
        
        # Populate location data if location_id exists
        if education.location:
            try:
                location = self.location_repo.get(education.location)
                if location:
                    education_dict['location'] = ReadLocation.model_validate(location).model_dump()
                else:
                    education_dict['location'] = None
            except:
                education_dict['location'] = None
        else:
            education_dict['location'] = None
        
        return ReadEducation.model_validate(education_dict)

    def _convert_list_to_read_dto(self, educations: List[Education]) -> List[ReadEducation]:
        """Convert list of Education database models to ReadEducation DTOs with populated locations"""
        return [self._convert_to_read_dto(edu) for edu in educations]

    def create_education(self, education_create: CreateEducation) -> ReadEducation:
        # Check if profile exists
        profile = self.session.get(Profile, education_create.profile_id)
        if not profile:
            raise ProfileNotFound(education_create.profile_id)
        
        # Handle location creation if provided
        location_id = None
        if education_create.location:
            location_data = education_create.location
            
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
        
        # Create education data excluding the location object
        education_data = education_create.dict(exclude_unset=True, exclude={'location'})
        education_data['location'] = location_id
        
        education = Education(**education_data)
        created_education = self.repo.create(education)
        return self._convert_to_read_dto(created_education)

    def get_education(self, education_id: UUID) -> ReadEducation:
        education = self.repo.get(education_id)
        if not education:
            raise EducationNotFound(education_id)
        return self._convert_to_read_dto(education)

    def get_educations_by_profile(self, profile_id: UUID) -> List[ReadEducation]:
        # Validate profile
        profile = self.session.get(Profile, profile_id)
        if not profile:
            raise ProfileNotFound(profile_id)

        educations = self.repo.get_by_profile_id(profile_id)
        return self._convert_list_to_read_dto(educations)


    def list_educations(self, skip: int = 0, limit: int = 20, profile_id: Optional[UUID] = None) -> List[ReadEducation]:
        educations = self.repo.list(skip=skip, limit=limit, profile_id=profile_id)
        return self._convert_list_to_read_dto(educations)

    def update_education(self, education_id: UUID, education_update: UpdateEducation) -> ReadEducation:
        education = self.repo.get(education_id)
        if not education:
            raise EducationNotFound(education_id)

        # Handle location update if provided
        if education_update.location is not None:
            if education_update.location:
                location_data = education_update.location
                
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
                        education.location = location_data.id
                    else:
                        # Location ID provided but doesn't exist - create new location
                        location = Location(**location_data.dict(exclude_unset=True, exclude={'id'}))
                        created_location = self.location_repo.create(location)
                        education.location = created_location.id
                else:
                    # No ID provided - create new location
                    location = Location(**location_data.dict(exclude_unset=True, exclude={'id'}))
                    created_location = self.location_repo.create(location)
                    education.location = created_location.id
            else:
                # Set location to None if explicitly provided as None
                education.location = None
        
        # Update other fields
        update_data = education_update.dict(exclude_unset=True, exclude={'location'})
        for key, value in update_data.items():
            setattr(education, key, value)
        
        updated_education = self.repo.update(education)
        return self._convert_to_read_dto(updated_education)

    def delete_education(self, education_id: UUID) -> str:
        education = self.repo.get(education_id)
        if not education:
            raise EducationNotFound(education_id)
        self.repo.delete(education)
        return f"Education {education_id} deleted successfully"

    def get_educations_by_profile_with_locations(self, profile_id: UUID) -> List[ReadEducation]:
        """
        Get all educations for a profile with their associated locations populated.
        Returns empty list if no educations found.
        """
        return self.get_educations_by_profile(profile_id)

    def get_educations_by_github_username(self, github_username: str) -> List[ReadEducation]:
        """Get all educations by GitHub username"""
        from Services.User.profile_service import ProfileService
        
        profile_service = ProfileService(self.session)
        profile_id = profile_service.get_profile_id_by_github_username(github_username)
        return self.get_educations_by_profile(profile_id)