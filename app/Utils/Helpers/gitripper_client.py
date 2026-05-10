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
