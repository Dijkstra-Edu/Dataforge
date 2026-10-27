from typing import Optional
import httpx

from Entities.Helios.repo_analysis import HelioRepoAnalysisResponse, RepoAnalysisDto


class HeliosClientError(Exception):
    pass

class HeliosClient():
    def __init__(self, base_url: str = "http://localhost:8070"):
        self.base_url = base_url.rstrip("/")

    def fetch_repo_stats_for_projects(self, github_user_id: str, repo_urls: list[str], timeout: float = 3.) -> list[RepoAnalysisDto]:
    
        url = f"{self.base_url}/user_metrics/projects"
        repo_names = [repo_url.split("/")[-1] for repo_url in repo_urls]
        try:
            response = httpx.post(url, json={"user_id": github_user_id, "repo_names": repo_names}, timeout=timeout)
        except Exception as e:
            raise HeliosClientError(f"Helios-service unreachable: {e}")

        if response.status_code != 200: #FIXME: Error handling not working correctly here
            raise HeliosClientError(
                f"Helios-service returned {response.status_code}: {response.text}"
            )

        data = response.json()

        return [RepoAnalysisDto.model_validate(ele) for ele in data]
        
        

    
    def fetch_repo_stats_for_project(self, repo_url: str, timeout: float = 3.0) -> Optional[HelioRepoAnalysisResponse]:
        url_parts = repo_url.rstrip("/").split("/")
        if len(url_parts) < 2:
            raise HeliosClientError(f"Invalid repository URL: {repo_url}")
        owner = url_parts[-2]
        repo = url_parts[-1]

        url = f"{self.base_url}/user_metrics/projects/{owner}/{owner}/{repo}"

        try:
            response = httpx.get(url, timeout=timeout)
        except Exception as e:
            raise HeliosClientError(f"Helios-service unreachable: {e}")

        if response.status_code != 200: #FIXME: Error handling not working correctly here
            raise HeliosClientError(
                f"Helios-service returned {response.status_code}: {response.text}"
            )

        data = response.json()
        return HelioRepoAnalysisResponse.model_validate(data)

