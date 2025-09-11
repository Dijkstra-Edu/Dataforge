# services/projects_opportunities_service.py
from uuid import UUID
from fastapi import HTTPException, status
from sqlmodel import Session
from Entities.SQL.Models.models import Organization, ProjectsOpportunities
from Repository.Opportunities.projects_opportunities_repository import ProjectsOpportunitiesRepository
from Schema.projects_opportunities_schema import CreateProject, UpdateProject
from Entities.SQL.Enums.enums import Tools

class ProjectsOpportunitiesService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = ProjectsOpportunitiesRepository(session)

    def create_project(self, project_create: CreateProject) -> ProjectsOpportunities:
        # Check if the organization exists
        org = self.session.get(Organization, project_create.organization)
        if not org:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Organization with ID {project_create.organization} does not exist."
            )
        
        # Validate languages
        if project_create.languages:
            invalid_langs = [
                lang for lang in project_create.languages
                if lang not in Tools._value2member_map_
            ]
            if invalid_langs:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid languages: {invalid_langs}. Must be one of {list(Tools)}"
                )
            
        # Validate frameworks
        if project_create.frameworks:
            invalid_frameworks = [
                framework for framework in project_create.frameworks
                if framework not in Tools._value2member_map_
            ]
            if invalid_frameworks:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid frameworks: {invalid_frameworks}. Must be one of {list(Tools)}"
                )
        
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

        # Validate languages if present
        if "languages" in update_data:
            invalid_langs = [
                lang for lang in update_data["languages"]
                if lang not in Tools._value2member_map_
            ]
            if invalid_langs:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid languages: {invalid_langs}. Must be one of {list(Tools)}"
                )
            
        # Validate frameworks if present
        if "frameworks" in update_data:
            invalid_frameworks = [
                framework for framework in update_data["frameworks"]
                if framework not in Tools._value2member_map_
            ]
            if invalid_frameworks:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid frameworks: {invalid_frameworks}. Must be one of {list(Tools)}"
                )

        for key, value in update_data.items():
            setattr(project, key, value)
        return self.repo.update(project)

    def delete_project(self, project_id: UUID):
        project = self.repo.get(project_id)
        if project:
            self.repo.delete(project)
        return project
