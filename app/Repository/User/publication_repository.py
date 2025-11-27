from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError

from Schema.SQL.Models.models import Publications


class PublicationRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, publication: Publications) -> Publications:
        try:
            self.session.add(publication)
            self.session.commit()
            self.session.refresh(publication)
            return publication
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def get(self, publication_id: UUID) -> Optional[Publications]:
        statement = select(Publications).where(Publications.id == publication_id)
        return self.session.exec(statement).first()

    def list(self, skip: int = 0, limit: int = 20) -> List[Publications]:
        statement = select(Publications).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def get_by_profile_id(self, profile_id: UUID) -> List[Publications]:
        statement = select(Publications).where(Publications.profile_id == profile_id)
        return self.session.exec(statement).all()

    def update(self, publication: Publications) -> Publications:
        try:
            self.session.add(publication)
            self.session.commit()
            self.session.refresh(publication)
            return publication
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def delete(self, publication: Publications):
        try:
            self.session.delete(publication)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise
