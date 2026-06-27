# services/projects_opportunities_service.py
from Settings.logging_config import get_logger
from typing import Optional
from uuid import UUID
from sqlmodel import Session
from Schema.SQL.Models.models import Organization, ProjectsOpportunities
from Repository.Opportunities.projects_opportunities_repository import ProjectsOpportunitiesRepository
from Entities.OpportunityDTOs.projects_opportunities_entity import CreateProject, PaginatedReadProjects, UpdateProject
from Schema.SQL.Enums.enums import Tools
from Utils.Exceptions.opportunities_exceptions import OrganizationNotFound, ProjectOpportunityNotFound
from Utils.Helpers.opportunities_helpers import _validate_tools
from Utils.Helpers.gitripper_client import GitRipperClient, GitRipperClientError
from datetime import date, datetime, timedelta

logger = get_logger()
class ProjectsOpportunitiesService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = ProjectsOpportunitiesRepository(session)

    def create_project(self, project_create: CreateProject) -> ProjectsOpportunities:
        # Check organization exists
        org = self.session.get(Organization, project_create.organization)
        if not org:
            raise OrganizationNotFound(project_create.organization)

        # Validate tools
        _validate_tools(project_create.languages, "languages")
        _validate_tools(project_create.frameworks, "frameworks")
        
        project = ProjectsOpportunities(**project_create.dict(exclude_unset=True))
        stats = self.fetch_project_github_data(project)
        logger.info("Hello from here")

        logger.info("Stats received:"+str(stats))
        logger.info("Hello from here")
        project.issues_count = stats["issuesCount"]
        project.stars = stats["stars"]
        project.forks = stats["forks"]
        project.last_updated = stats["lastUpdatedAt"]
        project.last_synced = date.today()
        return self.repo.create(project)

    def get_project(self, project_id: UUID) -> ProjectsOpportunities:
        project = self.repo.get(project_id)
        if not project:
            raise ProjectOpportunityNotFound(project_id)
        return project

    def list_projects(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: dict = {},
        sort_by: str = "created_at",
        order: str = "desc"
    ):
        projects, total = self.repo.list(skip=skip, limit=limit, filters=filters, sort_by=sort_by, order=order)
        for project in projects:
            if project.last_synced < datetime.now() - timedelta(days=10):
                stats = self.fetch_project_github_data(project)
                project.issues_count = stats["issuesCount"]
                project.stars = stats["stars"]
                project.forks = stats["forks"]
                project.last_updated = stats["lastUpdatedAt"]
                project.last_synced = date.today()
                self.repo.update(project)


        response = PaginatedReadProjects(
            total=total,
            projects=projects
            )
        
        return response
    
    def fetch_project_github_data(self, project: ProjectsOpportunities) -> dict:
        gitripper_client = GitRipperClient()
        try:
            return gitripper_client.fetch_repo_stats(project.repository)
        except GitRipperClientError as e:
            print(f"Error fetching stats for project {project.id}: {e}")
            return {"readme": None}

    def fetch_readme_for_project(self, project: ProjectsOpportunities) -> Optional[str]:
        gitripper_client = GitRipperClient()
        try:           
            readme_content = gitripper_client.fetch_readme(project.repository)
            return readme_content
        except GitRipperClientError as e:
            print(f"Error fetching README for project {project.id}: {e}")
            return None

    def autocomplete_projects(self, query: str, field: str = "title", limit: int = 10):
        return self.repo.autocomplete(query, field, limit)

    def update_project(self, project_id: UUID, project_update: UpdateProject) -> ProjectsOpportunities:
        project = self.repo.get(project_id)
        if not project:
            raise ProjectOpportunityNotFound(project_id)
        update_data = project_update.dict(exclude_unset=True)

         # Validate tools if present
        if "languages" in update_data:
            _validate_tools(update_data["languages"], "languages")
        if "frameworks" in update_data:
            _validate_tools(update_data["frameworks"], "frameworks")

        for key, value in update_data.items():
            setattr(project, key, value)
        return self.repo.update(project)

    def delete_project(self, project_id: UUID) -> Optional[str] :
        project = self.repo.get(project_id)
        if not project:
            raise ProjectOpportunityNotFound(project_id)
        self.repo.delete(project)
        return f"Project {project_id} deleted successfully"
    
    def get_filter_helpers(self) -> dict:
        return {
            "languages": self.repo.get_distinct_languages(),
            "categories": self.repo.get_distinct_categories(),
            "difficulties": self.repo.get_distinct_difficulties(),
            "licenses": self.repo.get_distinct_licenses()
        }