from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from sqlalchemy import asc, desc
from sqlalchemy.exc import SQLAlchemyError
from Schema.SQL.Models.models import Profile

class ProfileRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, profile: Profile) -> Profile:
        try:
            self.session.add(profile)
            self.session.commit()
            self.session.refresh(profile)
            return profile
        except SQLAlchemyError as e:
            self.session.rollback()
            raise

    def get(self, profile_id: UUID) -> Optional[Profile]:
        statement = select(Profile).where(Profile.id == profile_id)
        return self.session.exec(statement).first()

    def get_by_user_id(self, user_id: UUID) -> Optional[Profile]:
        statement = select(Profile).where(Profile.user_id == user_id)
        return self.session.exec(statement).first()

    def list(
        self,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        order: str = "desc",
        user_id: Optional[UUID] = None,
    ) -> List[Profile]:
        statement = select(Profile)

        # Filtering
        if user_id:
            statement = statement.where(Profile.user_id == user_id)

        # Sorting
        sort_column = getattr(Profile, sort_by, Profile.created_at)
        if order.lower() == "desc":
            statement = statement.order_by(desc(sort_column))
        else:
            statement = statement.order_by(asc(sort_column))

        # Pagination
        statement = statement.offset(skip).limit(limit)

        return self.session.exec(statement).all()

    def update(self, profile: Profile) -> Profile:
        try:
            self.session.add(profile)
            self.session.commit()
            self.session.refresh(profile)
            return profile
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def delete(self, profile: Profile):
        try:
            self.session.delete(profile)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise

    # Secondary Methods
    def get_with_user_details(self, profile_id: UUID) -> Optional[Profile]:
        statement = select(Profile).where(Profile.id == profile_id)
        return self.session.exec(statement).first()