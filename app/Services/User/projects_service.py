from uuid import UUID
from typing import List
from sqlmodel import Session

from Repository.User.projects_repository import ProjectsRepository
from Entities.UserDTOs.projects_entity import (
    CreateProject,
    ReadProject,
    UpdateProject,
)
from Schema.SQL.Models.models import Projects, Profile, User
from Utils.Exceptions.user_exceptions import (
    ProfileNotFound,
    ProjectsNotFound,
)

class ProjectsService:
    def __init__(self, session: Session):
        self.repo = ProjectsRepository(session)
        self.session = session

    def create_project(self, project_create: CreateProject) -> ReadProject:
        # Check if profile exists
        profile = self.session.get(Profile, project_create.profile_id)
        if not profile:
            raise ProfileNotFound(project_create.profile_id)

        # Create project if checks pass
        project = Projects(**project_create.dict(exclude_unset=True))
        project = self.repo.create(project)
        return ReadProject.model_validate(project)

    def get_project(self, project_id: UUID) -> ReadProject:
        project = self.repo.get(project_id)
        if not project:
            raise ProjectsNotFound(project_id)
        return ReadProject.model_validate(project)

    def list_projects(self, skip: int = 0, limit: int = 20) -> List[ReadProject]:
        projects = self.repo.list(skip=skip, limit=limit)
        return [ReadProject.model_validate(proj) for proj in projects]

    def get_projects_by_profile(self, profile_id: UUID) -> List[ReadProject]:
        projects = self.repo.get_by_profile(profile_id)
        return [ReadProject.model_validate(proj) for proj in projects]

    def update_project(
        self, project_id: UUID, project_update: UpdateProject
    ) -> ReadProject:
        project = self.repo.get(project_id)
        if not project:
            raise ProjectsNotFound(project_id)

        update_data = project_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(project, key, value)

        updated_project = self.repo.update(project)
        return ReadProject.model_validate(updated_project)

    def delete_project(self, project_id: UUID) -> str:
        project = self.repo.get(project_id)
        if not project:
            raise ProjectsNotFound(project_id)

        self.repo.delete(project)
        return f"Project with ID {project_id} deleted successfully."
