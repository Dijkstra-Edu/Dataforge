# Repository/users_repository.py

from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from sqlalchemy import asc, desc
from Entities.SQL.Models.models import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get(self, user_id: UUID) -> Optional[User]:
        statement = select(User).where(User.id == user_id)
        return self.session.exec(statement).first()

    def get_by_github_username(self, github_user_name: str) -> Optional[User]:
        statement = select(User).where(User.github_user_name == github_user_name)
        return self.session.exec(statement).first()

    def list(
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
        statement = select(User)

        # Filtering
        if first_name:
            statement = statement.where(User.first_name.ilike(f"%{first_name}%"))
        if last_name:
            statement = statement.where(User.last_name.ilike(f"%{last_name}%"))
        if github_user_name:
            statement = statement.where(User.github_user_name.ilike(f"%{github_user_name}%"))
        if rank:
            statement = statement.where(User.rank == rank)
        if min_streak is not None:
            statement = statement.where(User.streak >= min_streak)
        if max_streak is not None:
            statement = statement.where(User.streak <= max_streak)

        # Sorting
        sort_column = getattr(User, sort_by, User.created_at)
        if order.lower() == "desc":
            statement = statement.order_by(desc(sort_column))
        else:
            statement = statement.order_by(asc(sort_column))

        # Pagination
        statement = statement.offset(skip).limit(limit)

        return self.session.exec(statement).all()

    def autocomplete(self, query: str, field: str = "github_user_name", limit: int = 10) -> List[User]:
        """
        Autocomplete based on a given field (default: github_user_name).
        """
        field_column = getattr(User, field, User.github_user_name)
        statement = (
            select(User)
            .where(field_column.ilike(f"%{query}%"))
            .limit(limit)
        )
        return self.session.exec(statement).all()

    def update(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user: User):
        self.session.delete(user)
        self.session.commit()
