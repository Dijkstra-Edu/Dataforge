from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError

from Schema.SQL.Models.models import Education


class EducationRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, education: Education) -> Education:
        try:
            self.session.add(education)
            self.session.commit()
            self.session.refresh(education)
            return education
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def get(self, education_id: UUID) -> Optional[Education]:
        statement = select(Education).where(Education.id == education_id)
        return self.session.exec(statement).first()

    def get_by_profile_id(self, profile_id: UUID) -> List[Education]:
        statement = select(Education).where(Education.profile_id == profile_id)
        return self.session.exec(statement).all()

    def list(self, skip: int = 0, limit: int = 20, profile_id: Optional[UUID] = None) -> List[Education]:
        statement = select(Education)
        if profile_id:
            statement = statement.where(Education.profile_id == profile_id)

        statement = statement.offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def update(self, education: Education) -> Education:
        try:
            self.session.add(education)
            self.session.commit()
            self.session.refresh(education)
            return education
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def delete(self, education: Education):
        try:
            self.session.delete(education)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise