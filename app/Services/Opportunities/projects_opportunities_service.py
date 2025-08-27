# services/projects_opportunities_service.py
from uuid import UUID
from sqlmodel import Session
from Entities.SQL.Models.models import ProjectsOpportunities
from Repository.Opportunities.projects_opportunities_repository import ProjectsOpportunitiesRepository
from Schema.projects_opportunities_schema import CreateProject, UpdateProject

class ProjectsOpportunitiesService:
    def __init__(self, session: Session):
        self.repo = ProjectsOpportunitiesRepository(session)

    def create_project(self, project_create: CreateProject) -> ProjectsOpportunities:
        project = ProjectsOpportunities(**project_create.dict(exclude_unset=True))
        return self.repo.create(project)

    def get_project(self, project_id: UUID) -> ProjectsOpportunities:
        return self.repo.get(project_id)

    def list_projects(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: dict = {},
        sort_by: str = "created_at",
        order: str = "desc"
    ):
        return self.repo.list(skip=skip, limit=limit, filters=filters, sort_by=sort_by, order=order)

    def autocomplete_projects(self, query: str, field: str = "title", limit: int = 10):
        return self.repo.autocomplete(query, field, limit)

    def update_project(self, project_id: UUID, project_update: UpdateProject) -> ProjectsOpportunities:
        project = self.repo.get(project_id)
        if not project:
            return None
        update_data = project_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(project, key, value)
        return self.repo.update(project)

    def delete_project(self, project_id: UUID):
        project = self.repo.get(project_id)
        if project:
            self.repo.delete(project)
        return project
