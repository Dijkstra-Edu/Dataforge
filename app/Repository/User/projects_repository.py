from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError
from Schema.SQL.Models.models import Projects


class ProjectsRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, project: Projects) -> Projects:
        try:
            self.session.add(project)
            self.session.commit()
            self.session.refresh(project)
            return project
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def get(self, project_id: UUID) -> Optional[Projects]:
        statement = select(Projects).where(Projects.id == project_id)
        return self.session.exec(statement).first()

    def list(self, skip: int = 0, limit: int = 20) -> List[Projects]:
        statement = select(Projects).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def get_by_profile(self, profile_id: UUID) -> List[Projects]:
        statement = select(Projects).where(Projects.profile_id == profile_id)
        return self.session.exec(statement).all()

    def update(self, project: Projects) -> Projects:
        try:
            self.session.add(project)
            self.session.commit()
            self.session.refresh(project)
            return project
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def delete(self, project: Projects):
        try:
            self.session.delete(project)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise