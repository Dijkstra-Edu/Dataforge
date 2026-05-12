from uuid import UUID
from typing import List
from sqlmodel import Session

from Repository.User.projects_repository import ProjectsRepository
from Entities.UserDTOs.projects_entity import (
    CreateProject,
    ReadProject,
    UpdateProject,
)
from Schema.SQL.Models.models import Projects
from Utils.Exceptions.user_exceptions import (ProjectsNotFound)
from Services.User.profile_service import ProfileService

class ProjectsService:
    def __init__(self, session: Session):
        self.repo = ProjectsRepository(session)
        self.session = session

    def create_project(self, project_create: CreateProject) -> ReadProject:
        profile_service = ProfileService(self.session)
        profile_id = profile_service.get_profile_id_by_github_username(project_create.username)

        # Create project if checks pass
        project_data = project_create.dict(exclude_unset=True)
        project_data.pop("username", None)
        project_data["profile_id"] = profile_id
        project = Projects(**project_data)
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
    
    def get_projects_by_github_username(self, github_username: str) -> List[ReadProject]:
        """Get all projects by GitHub username"""        
        profile_service = ProfileService(self.session)
        profile_id = profile_service.get_profile_id_by_github_username(github_username)
        return self.get_projects_by_profile(profile_id)

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
