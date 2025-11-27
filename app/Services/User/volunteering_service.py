from uuid import UUID
from typing import List, Optional
from sqlmodel import Session

from Schema.SQL.Models.models import Volunteering, Profile
from Repository.User.volunteering_repository import VolunteeringRepository
from Entities.UserDTOs.volunteering_entity import CreateVolunteering, UpdateVolunteering
from Utils.Exceptions.user_exceptions import ProfileNotFound, VolunteeringNotFound


class VolunteeringService:
    def __init__(self, session: Session):
        self.repo = VolunteeringRepository(session)
        self.session = session

    def create_volunteering(self, volunteering_create: CreateVolunteering) -> Volunteering:
        # Ensure profile exists
        profile = self.session.get(Profile, volunteering_create.profile_id)
        if not profile:
            raise ProfileNotFound(volunteering_create.profile_id)

        volunteering = Volunteering(**volunteering_create.dict(exclude_unset=True))
        return self.repo.create(volunteering)

    def get_volunteering(self, volunteering_id: UUID) -> Volunteering:
        volunteering = self.repo.get(volunteering_id)
        if not volunteering:
            raise VolunteeringNotFound(volunteering_id)
        return volunteering

    def list_volunteering(self, skip: int = 0, limit: int = 20) -> List[Volunteering]:
        return self.repo.list(skip=skip, limit=limit)

    def get_volunteering_by_profile_id(self, profile_id: UUID) -> List[Volunteering]:
        volunteering_entries = self.repo.get_by_profile_id(profile_id)
        if not volunteering_entries:
            raise VolunteeringNotFound(profile_id)
        return volunteering_entries
    
    def get_volunteering_by_github_username(self, github_username: str) -> List[Volunteering]:
        """Get all volunteering by GitHub username"""
        from Services.User.profile_service import ProfileService
        
        profile_service = ProfileService(self.session)
        profile_id = profile_service.get_profile_id_by_github_username(github_username)
        return self.get_volunteering_by_profile_id(profile_id)

    def update_volunteering(self, volunteering_id: UUID, volunteering_update: UpdateVolunteering) -> Volunteering:
        volunteering = self.repo.get(volunteering_id)
        if not volunteering:
            raise VolunteeringNotFound(volunteering_id)

        # If profile_id is updated, ensure the profile exists
        if volunteering_update.profile_id and volunteering_update.profile_id != volunteering.profile_id:
            profile = self.session.get(Profile, volunteering_update.profile_id)
            if not profile:
                raise ProfileNotFound(volunteering_update.profile_id)

        update_data = volunteering_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(volunteering, key, value)

        return self.repo.update(volunteering)

    def delete_volunteering(self, volunteering_id: UUID) -> str:
        volunteering = self.repo.get(volunteering_id)
        if not volunteering:
            raise VolunteeringNotFound(volunteering_id)

        self.repo.delete(volunteering)
        return f"Volunteering {volunteering_id} deleted successfully"
