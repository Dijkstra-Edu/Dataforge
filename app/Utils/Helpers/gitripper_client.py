from typing import Optional
import httpx


class GitRipperClientError(Exception):
    pass

class GitRipperClient():
    def __init__(self, base_url: str = "http://localhost:7060"):
        self.base_url = base_url.rstrip("/")

    def sync_user(
        self,
        login_id: str,
        email: str,
        timeout: float = 3.0,
    ) -> None:

        payload = {
            "loginId": login_id,
            "email": email,
        }

        url = f"{self.base_url}/user/create"

        try:
            response = httpx.post(url, json=payload, timeout=timeout)
        except Exception as e:
            raise GitRipperClientError(f"User-service unreachable: {e}")

        if response.status_code >= 300:
            raise GitRipperClientError(
                f"User-service returned {response.status_code}: {response.text}"
            )

    def fetch_readme(self, repo_url: str, timeout: float = 3.0) -> Optional[str]:
        url_parts = repo_url.rstrip("/").split("/")
        if len(url_parts) < 2:
            raise GitRipperClientError(f"Invalid repository URL: {repo_url}")
        owner = url_parts[-2]
        repo = url_parts[-1]

        url = f"{self.base_url}/repo/{owner}/{repo}/readme"

        try:
            response = httpx.get(url, timeout=timeout)
        except Exception as e:
            raise GitRipperClientError(f"User-service unreachable: {e}")

        if response.status_code != 200: #FIXME: Error handling not working correctly here
            raise GitRipperClientError(
                f"User-service returned {response.status_code}: {response.text}"
            )

        data = response.json()
        return data.get("content")
    
    def fetch_repo_stats(self, repo_url: str, timeout: float = 3.0) -> Optional[str]:
        url_parts = repo_url.rstrip("/").split("/")
        if len(url_parts) < 2:
            raise GitRipperClientError(f"Invalid repository URL: {repo_url}")
        owner = url_parts[-2]
        repo = url_parts[-1]

        url = f"{self.base_url}/repo/{owner}/{repo}/stats"

        try:
            response = httpx.get(url, timeout=timeout)
        except Exception as e:
            raise GitRipperClientError(f"User-service unreachable: {e}")

        if response.status_code != 200: #FIXME: Error handling not working correctly here
            raise GitRipperClientError(
                f"User-service returned {response.status_code}: {response.text}"
            )

        data = response.json()
        return data
