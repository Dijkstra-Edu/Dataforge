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
from Utils.Exceptions.user_exceptions import (ProjectAlreadyExists, ProjectsNotFound)
from Services.User.profile_service import ProfileService
from Utils.Helpers.gitripper_client import GitRipperClient
from Utils.Helpers.helios_client import HeliosClient

class ProjectsService:
    def __init__(self, session: Session):
        self.repo = ProjectsRepository(session)
        self.session = session

    def _convert_to_read_dto(self, project: Projects, enrich_project: bool = False) -> ReadProject:
            project_dict = project.dict()
            project_dict['username'] = project.profile_rel.username
            if enrich_project:
                self.enrich_project(project_dict)
            return ReadProject.model_validate(project_dict)

    def _convert_list_to_read_dtos(self, github_username: str, projects: List[Projects], enrich_projects: bool = False) -> List[ReadProject]:
            project_dicts = []
            for project in projects:
                project_dict = project.dict()
                project_dict['username'] = project.profile_rel.username
                project_dicts.append(project_dict)
            if enrich_projects:
                self.enrich_projects_for_user(github_username, project_dicts)
            res = [ReadProject.model_validate(project_dict) for project_dict in project_dicts]
            return res
    
    #Should this even exist or should we directly populate this from github?
    def create_project(self, project_create: CreateProject) -> ReadProject:
        profile_service = ProfileService(self.session)
        profile_id = profile_service.get_profile_id_by_github_username(project_create.username)
        existing_project = self.repo.find_by_repo_url(project_create.github_repo_url)
        if existing_project:
            raise ProjectAlreadyExists(project_create.github_repo_url)
        # Create project if checks pass
        project_data = project_create.dict(exclude_unset=True)
        project_data.pop("username", None)
        project_data["profile_id"] = profile_id
        project = Projects(**project_data)
        project = self.repo.create(project)
        return self._convert_to_read_dto(project)

    def get_project(self, project_id: UUID) -> ReadProject:
        project = self.repo.get(project_id)
        if not project:
            raise ProjectsNotFound(project_id)
        return self._convert_to_read_dto(project, True)

    def enrich_projects_for_user(self, github_username: str, projects: List[dict]):
        self.enrich_projects_with_helios_stats(github_username, projects)
        self.enrich_projects_with_repo_stats(github_username, projects)


    def enrich_project(self, project: dict):
        self.enrich_project_with_repo_stats(project)
        self.enrich_project_with_helios_stats(project)
        
    def enrich_project_with_repo_stats(self, project: dict):
        gitRipperClient = GitRipperClient()
        github_repo_stats =  gitRipperClient.fetch_repo_stats(project['github_repo_url'])
        project['github_stars'] = github_repo_stats.stars
        project['github_open_issues'] = github_repo_stats.issuesCount
        project['github_forks'] = github_repo_stats.forks
        project['total_lines_contributed'] = github_repo_stats.ownerLineContribution
    
        
    def enrich_project_with_helios_stats(self, project: dict):
        heliosClient = HeliosClient()
        repo_analysis = heliosClient.fetch_repo_stats_for_project(project['github_repo_url'])
        if repo_analysis.exists:
            project['repo_analysis'] = repo_analysis.analysis.dict()

    def enrich_projects_with_helios_stats(self, github_username: str, projects: List[dict]):
        heliosClient = HeliosClient()
        project_map = {project['github_repo_url']: project for project in projects}
        repo_analysis_list = heliosClient.fetch_repo_stats_for_projects(github_username, project_map.keys())
        for repo_analysis in repo_analysis_list:
                if repo_analysis.repo_url in project_map:
                    project_map[repo_analysis.repo_url]['repo_analysis'] = repo_analysis.dict()

    def enrich_projects_with_repo_stats(self, github_username: str, projects: List[dict]):
        gitRipperClient = GitRipperClient()
        project_map = {project['github_repo_url']: project for project in projects}
        repo_stats = gitRipperClient.fetch_stats_for_repos(github_username, list(project_map.keys()))
        for repo_stat in repo_stats:
            repo_url = "https://github.com/" + repo_stat.owner + "/" + repo_stat.name
            if repo_url in project_map:
                project = project_map[repo_url]
                project['github_stars'] = repo_stat.stars
                project['github_open_issues'] = repo_stat.issuesCount
                project['github_forks'] = repo_stat.forks
                project['total_lines_contributed'] = repo_stat.ownerLineContribution


    def list_projects(self, skip: int = 0, limit: int = 20) -> List[ReadProject]:
        projects = self.repo.list(skip=skip, limit=limit)
        if len(projects) == 0:
            return []
        github_username = projects[0].profile_rel.username
        return self._convert_list_to_read_dtos(github_username, projects, True)

    def get_projects_by_profile(self, profile_id: UUID) -> List[ReadProject]:
        projects = self.repo.get_by_profile(profile_id)
        if len(projects) == 0:
            return []
        github_username = projects[0].profile_rel.username
        return self._convert_list_to_read_dtos(github_username, projects, True)
    
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
        return self._convert_to_read_dto(updated_project)

    def delete_project(self, project_id: UUID) -> str:
        project = self.repo.get(project_id)
        if not project:
            raise ProjectsNotFound(project_id)

        self.repo.delete(project)
        return f"Project with ID {project_id} deleted successfully."
