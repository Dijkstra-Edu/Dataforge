# Services/users_service.py

from uuid import UUID
from typing import List, Optional
from sqlmodel import Session
from Repository.User.user_repository import UserRepository
from Schema.user_schema import CreateUser, UpdateUser
from Entities.SQL.Models.models import User


class UserService:
    def __init__(self, session: Session):
        self.repo = UserRepository(session)

    def create_user(self, user_create: CreateUser) -> User:
        # Check if github username already exists
        existing_user = self.repo.get_by_github_username(user_create.github_user_name)
        if existing_user:
            raise ValueError(f"User with github username '{user_create.github_user_name}' already exists")
        
        user = User(**user_create.dict(exclude_unset=True))
        return self.repo.create(user)

    def get_user(self, user_id: UUID) -> Optional[User]:
        return self.repo.get(user_id)

    def get_user_by_github_username(self, github_user_name: str) -> Optional[User]:
        return self.repo.get_by_github_username(github_user_name)

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
            return None
        
        # Check if github username is being updated and if it already exists
        if user_update.github_user_name and user_update.github_user_name != user.github_user_name:
            existing_user = self.repo.get_by_github_username(user_update.github_user_name)
            if existing_user:
                raise ValueError(f"User with github username '{user_update.github_user_name}' already exists")
        
        update_data = user_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        return self.repo.update(user)

    def delete_user(self, user_id: UUID) -> Optional[User]:
        user = self.repo.get(user_id)
        if user:
            self.repo.delete(user)
        return user