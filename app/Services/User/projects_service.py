from uuid import UUID
from typing import List

from sqlmodel import Session

from Repository.User.projects_repository import ProjectsRepository
from Entities.UserDTOs.projects_entity import (
    CreateProject,
    ReadProject,
    UpdateProject,
)
from Utils.Exceptions.user_exceptions import ProfileNotFound, ServiceError


class ProjectsService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = ProjectsRepository(session)

    def create_project(self, project_create: CreateProject) -> ReadProject:
        try:
            project = self.repository.create(project_create)
            return ReadProject.model_validate(project)
        except ProfileNotFound as e:
            raise e
        except Exception as e:
            raise ServiceError(f"Failed to create project: {str(e)}")


    def get_project(self, project_id: UUID) -> ReadProject:
        project = self.repository.get(project_id)
        if not project:
            raise ServiceError(f"Project with ID {project_id} does not exist.")
        return ReadProject.model_validate(project)


    def list_projects(self, skip: int = 0, limit: int = 20) -> List[ReadProject]:
        projects = self.repository.list(skip=skip, limit=limit)
        return [ReadProject.model_validate(proj) for proj in projects]


    def get_projects_by_profile(self, profile_id: UUID) -> List[ReadProject]:
        projects = self.repository.get_by_profile(profile_id)
        return [ReadProject.model_validate(proj) for proj in projects]

    def update_project(self, project_id: UUID, project_update: UpdateProject) -> ReadProject:
        project = self.repository.update(project_id, project_update)
        if not project:
            raise ServiceError(f"Project with ID {project_id} does not exist.")
        return ReadProject.model_validate(project)


    def delete_project(self, project_id: UUID) -> str:
        deleted = self.repository.delete(project_id)
        if not deleted:
            raise ServiceError(f"Project with ID {project_id} does not exist.")
        return f"Project with ID {project_id} deleted successfully."
