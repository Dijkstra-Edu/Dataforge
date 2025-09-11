from uuid import UUID
from sqlmodel import Session, select
from typing import List, Optional


from Entities.UserDTOs.profile_entity import CreateProfile, UpdateProfile
from Schema.SQL.Models.models import Profile, User
from Repository.User.profile_repository import ProfileRepository
from Utils.Exceptions.user_exceptions import ProfileAlreadyExists, ProfileNotFound, ProfileNotFound, UserNotFound

class ProfileService:
    def __init__(self, session: Session):
        self.repo = ProfileRepository(session)
        self.session = session

    def create_profile(self, profile_create: CreateProfile) -> Profile:
        # Check if user exists
        user = self.session.get(User, profile_create.user_id)
        if not user:
            raise UserNotFound(profile_create.user_id)
        
        # Check if profile already exists for this user
        existing_profile = self.repo.get_by_user_id(profile_create.user_id)
        if existing_profile:
            raise ProfileAlreadyExists(profile_create.user_id)
        
        profile = Profile(**profile_create.dict(exclude_unset=True))
        return self.repo.create(profile)

    def get_profile(self, profile_id: UUID) -> Optional[Profile]:
        profile = self.repo.get(profile_id)
        if not profile:
            return ProfileNotFound(profile_id)
        return profile

    def get_profile_by_user_id(self, user_id: UUID) -> Optional[Profile]:
        profile = self.repo.get_by_user_id(user_id)
        if not profile:
            return ProfileNotFound(user_id)
        return profile

    def list_profiles(
        self,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        order: str = "desc",
        user_id: Optional[UUID] = None,
    ) -> List[Profile]:
        """
        Supports pagination, filtering, and sorting.
        """
        return self.repo.list(
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            order=order,
            user_id=user_id,
        )

    def update_profile(self, profile_id: UUID, profile_update: UpdateProfile) -> Optional[Profile]:
        profile = self.repo.get(profile_id)
        if not profile:
            return ProfileNotFound(profile_id)

        # Check if user_id is being updated and if the new user exists
        if profile_update.user_id and profile_update.user_id != profile.user_id:
            user = self.session.get(User, profile_update.user_id)
            if not user:
                raise UserNotFound(profile_update.user_id)

            # Check if profile already exists for the new user
            existing_profile = self.repo.get_by_user_id(profile_update.user_id)
            if existing_profile:
                raise ProfileAlreadyExists(profile_update.user_id)

        update_data = profile_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(profile, key, value)
        return self.repo.update(profile)

    def delete_profile(self, profile_id: UUID) -> Optional[str]:
        profile = self.repo.get(profile_id)
        if not profile:
            return ProfileNotFound(profile_id)
        self.repo.delete(profile)
        return f"Profile with ID {profile_id} deleted successfully."

    # Secondary Methods
    def get_profile_with_user_details(self, profile_id: UUID) -> Optional[Profile]:
        profile = self.repo.get_with_user_details(profile_id)
        if profile:
            # This will load the user relationship if it's not already loaded
            # You might need to adjust this based on your actual relationship setup
            return profile
        return None