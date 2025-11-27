from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError

from Schema.SQL.Models.models import Volunteering


class VolunteeringRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, volunteering: Volunteering) -> Volunteering:
        try:
            self.session.add(volunteering)
            self.session.commit()
            self.session.refresh(volunteering)
            return volunteering
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def get(self, volunteering_id: UUID) -> Optional[Volunteering]:
        statement = select(Volunteering).where(Volunteering.id == volunteering_id)
        return self.session.exec(statement).first()

    def list(self, skip: int = 0, limit: int = 20) -> List[Volunteering]:
        statement = select(Volunteering).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def get_by_profile_id(self, profile_id: UUID) -> List[Volunteering]:
        statement = select(Volunteering).where(Volunteering.profile_id == profile_id)
        return self.session.exec(statement).all()

    def update(self, volunteering: Volunteering) -> Volunteering:
        try:
            self.session.add(volunteering)
            self.session.commit()
            self.session.refresh(volunteering)
            return volunteering
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def delete(self, volunteering: Volunteering):
        try:
            self.session.delete(volunteering)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise
