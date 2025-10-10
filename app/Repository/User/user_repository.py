# Repository/users_repository.py

from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from sqlalchemy import asc, desc
from Schema.SQL.Models.models import User
from sqlalchemy.exc import SQLAlchemyError

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> User:
        try:
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user
        except SQLAlchemyError as e:
            self.session.rollback()
            raise

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
        try:
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def delete(self, user: User):
        try:
            self.session.delete(user)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def check_onboarding_by_github_username(self, github_user_name: str) -> tuple[bool, Optional[UUID]]:
        """
        Check if a user has completed onboarding by github username.
        Returns (onboarded_status, user_id)
        """
        statement = select(User.id, User.onboarding_complete).where(User.github_user_name == github_user_name)
        result = self.session.exec(statement).first()
        
        if result:
            user_id, onboarding_complete = result
            return (onboarding_complete, user_id)
        return (False, None)