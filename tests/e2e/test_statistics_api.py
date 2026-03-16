"""E2E API tests for statistics routes (full app, external HTTP mocked)."""
import pytest
from unittest.mock import patch, MagicMock

from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.mark.e2e
class TestStatisticsApiE2E:
    """End-to-end tests for /Dijkstra/v1/statistics/*."""

    def test_health_endpoint_no_mocks(self, client: TestClient):
        response = client.get("/Dijkstra/v1/statistics/health")
        assert response.status_code == 200
        assert response.json().get("message") == "Dijkstra Statistics Health Endpoint Triggered!!!"

    def test_github_endpoint_returns_structure(self, client: TestClient):
        response = client.get("/Dijkstra/v1/statistics/github/anyuser")
        assert response.status_code == 200
        data = response.json()
        assert "general_data" in data
        assert "dijkstra_statistics" in data
        assert "overall_github_statistics" in data

    def test_lc_endpoint_with_mocked_leetcode_api(self, client: TestClient):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {
                "matchedUser": {"username": "e2euser"},
                "userContestRanking": None,
            }
        }
        with patch(
            "Services.User.leetcode_service.requests.post",
            return_value=mock_response,
        ):
            response = client.get("/Dijkstra/v1/statistics/lc/e2euser")

        assert response.status_code == 200
        data = response.json()
        assert "leetcode" in data
        assert data["leetcode"].get("profile", {}).get("username") == "e2euser"
