# Services/users_service.py

from uuid import UUID
from typing import List, Optional
from sqlmodel import Session
from Repository.User.user_repository import UserRepository
from Repository.User.profile_repository import ProfileRepository
from Repository.User.links_repository import LinksRepository
from Entities.UserDTOs.user_entity import CreateUser, UpdateUser, OnboardUser, OnboardCheckResponse
from Schema.SQL.Models.models import User, Profile, Links
from Utils.Exceptions.user_exceptions import GitHubUsernameAlreadyExists, GitHubUsernameNotFound, UserNotFound


class UserService:
    def __init__(self, session: Session):
        self.repo = UserRepository(session)
        self.profile_repo = ProfileRepository(session)
        self.links_repo = LinksRepository(session)
        self.session = session

    def create_user(self, user_create: CreateUser) -> User:
        # Check if github username already exists
        existing_user = self.repo.get_by_github_username(user_create.github_user_name)
        if existing_user:
            raise GitHubUsernameAlreadyExists(user_create.github_user_name)
        
        user = User(**user_create.dict(exclude_unset=True))
        return self.repo.create(user)

    def get_user(self, user_id: UUID) -> Optional[User]:
        user = self.repo.get(user_id)
        if not user:
            return UserNotFound(user_id)
        return user

    def get_user_by_github_username(self, github_user_name: str) -> Optional[User]:
        user = self.repo.get_by_github_username(github_user_name)
        if not user:
            return GitHubUsernameNotFound(github_user_name)
        return user

    def list_users(
        self,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        order: str = "desc",
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        github_user_name: Optional[str] = None,
        rank: Optional[str] = None,
        min_streak: Optional[int] = None,
        max_streak: Optional[int] = None,
    ) -> List[User]:
        """
        Supports pagination, filtering, and sorting.
        """
        return self.repo.list(
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            order=order,
            first_name=first_name,
            last_name=last_name,
            github_user_name=github_user_name,
            rank=rank,
            min_streak=min_streak,
            max_streak=max_streak,
        )

    def autocomplete_users(
        self,
        query: str,
        field: str = "github_user_name",
        limit: int = 10,
    ) -> List[User]:
        """
        Returns users where the given field starts with or contains query text.
        """
        return self.repo.autocomplete(query=query, field=field, limit=limit)

    def update_user(self, user_id: UUID, user_update: UpdateUser) -> Optional[User]:
        user = self.repo.get(user_id)
        if not user:
            return UserNotFound(user_id)
        
        # Check if github username is being updated and if it already exists
        if user_update.github_user_name and user_update.github_user_name != user.github_user_name:
            existing_user = self.repo.get_by_github_username(user_update.github_user_name)
            if existing_user:
                raise GitHubUsernameAlreadyExists(user_update.github_user_name)
        
        update_data = user_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        return self.repo.update(user)

    def delete_user(self, user_id: UUID) -> Optional[str]:
        user = self.repo.get(user_id)
        if not user:
            return UserNotFound(user_id)
        self.repo.delete(user)
        return f"User {user_id} deleted successfully"

    def check_onboarding_status(self, github_user_name: str) -> OnboardCheckResponse:
        """
        Check if a user has completed onboarding by github username.
        Returns OnboardCheckResponse with onboarded status and user_id if found.
        """
        onboarded, user_id = self.repo.check_onboarding_by_github_username(github_user_name)
        return OnboardCheckResponse(onboarded=onboarded, user_id=user_id)

    def onboard_user(self, onboard_data: OnboardUser) -> User:
        """
        Create a new user with onboarding_complete=True, an empty Profile, and Links.
        This is an atomic operation - User, Profile, and Links are created together.
        """
        # Check if github username already exists
        existing_user = self.repo.get_by_github_username(onboard_data.github_user_name)
        if existing_user:
            raise GitHubUsernameAlreadyExists(onboard_data.github_user_name)
        
        try:
            # Create user with onboarding_complete=True
            user_dict = onboard_data.dict(exclude_unset=True, exclude={'linkedin_user_name', 'leetcode_user_name'})
            user_dict['onboarding_complete'] = True
            user_dict['data_loaded'] = False
            user = User(**user_dict)
            
            # Create user in database
            created_user = self.repo.create(user)
            
            # Create empty profile for the user
            profile = Profile(user_id=created_user.id)
            self.profile_repo.create(profile)
            
            # Create links for the user with auto-generated URLs
            links = Links(
                user_id=created_user.id,
                github_user_name=onboard_data.github_user_name,
                github_link=f"https://github.com/{onboard_data.github_user_name}",
                linkedin_user_name=onboard_data.linkedin_user_name,
                linkedin_link=None,
                leetcode_user_name=onboard_data.leetcode_user_name,
                leetcode_link=f"https://leetcode.com/u/{onboard_data.leetcode_user_name}",
            )
            self.links_repo.create(links)
            
            # Refresh to get the updated user with relationships
            self.session.refresh(created_user)
            
            return created_user
        except Exception as e:
            # If anything fails, rollback will happen in repository layer
            raise