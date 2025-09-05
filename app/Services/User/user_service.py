# Services/users_service.py

from uuid import UUID
from typing import List, Optional
from sqlmodel import Session
from Repository.users_repository import UserRepository
from Schema.users_schema import CreateUser, UpdateUser
from Entities.SQL.Models.models import User


class UserService:
    def __init__(self, session: Session):
        self.repo = UserRepository(session)

    def create_user(self, user_create: CreateUser) -> User:
        user = User(**user_create.dict(exclude_unset=True))
        return self.repo.create(user)

    def get_user(self, user_id: UUID) -> Optional[User]:
        return self.repo.get(user_id)

    def get_user_by_github(self, github_user_name: str) -> Optional[User]:
        return self.repo.get_by_github(github_user_name)

    def list_users(
        self,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        order: str = "desc",
        github_user_name: Optional[str] = None,
        rank: Optional[str] = None,
    ) -> List[User]:
        return self.repo.list(
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            order=order,
            github_user_name=github_user_name,
            rank=rank,
        )

    def autocomplete_users(self, query: str, field: str = "github_user_name", limit: int = 10) -> List[User]:
        return self.repo.autocomplete(query=query, field=field, limit=limit)

    def update_user(self, user_id: UUID, user_update: UpdateUser) -> Optional[User]:
        user = self.repo.get(user_id)
        if not user:
            return None
        update_data = user_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        return self.repo.update(user)

    def delete_user(self, user_id: UUID) -> Optional[User]:
        user = self.repo.get(user_id)
        if user:
            self.repo.delete(user)
        return user
