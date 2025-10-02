from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from Schema.SQL.Models.models import Projects , Profile 
from Entities.UserDTOs.projects_entity import CreateProject, UpdateProject
from Utils.Exceptions.user_exceptions import ProfileNotFound


class ProjectsRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, project_create: CreateProject) -> Projects:
        # Ensure profile exists
        profile = self.session.get(Profile, project_create.profile_id)
        if not profile:
            raise ProfileNotFound(project_create.profile_id)

        project = Projects(**project_create.dict(exclude_unset=True))
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)
        return project

    def get(self, project_id: UUID) -> Optional[Projects]:
        statement = select(Projects).where(Projects.id == project_id)
        result = self.session.exec(statement).first()
        return result


    def list(self, skip: int = 0, limit: int = 20) -> List[Projects]:
        statement = select(Projects).offset(skip).limit(limit)
        results = self.session.exec(statement).all()
        return results


    def get_by_profile(self, profile_id: UUID) -> List[Projects]:
        statement = select(Projects).where(Projects.profile_id == profile_id)
        results = self.session.exec(statement).all()
        return results

    def update(self, project_id: UUID, project_update: UpdateProject) -> Optional[Projects]:
        project = self.get(project_id)
        if not project:
            return None

        update_data = project_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(project, key, value)

        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)
        return project


    def delete(self, project_id: UUID) -> bool:
        project = self.get(project_id)
        if not project:
            return False

        self.session.delete(project)
        self.session.commit()
        return True
