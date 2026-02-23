"""Integration tests for statistics controller (router + mocked services)."""
import pytest
from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.mark.integration
class TestStatisticsController:
    """Statistics routes with patched GitHubService and LeetCodeService."""

    def test_health_returns_200_and_message(self, client: TestClient):
        response = client.get("/Dijkstra/v1/statistics/health")
        assert response.status_code == 200
        data = response.json()
        assert data.get("status") == 200
        assert "Dijkstra Statistics Health" in data.get("message", "")

    def test_github_returns_patched_service_response(self, client: TestClient):
        mock_data = {"general_data": {"username": "testuser"}, "dijkstra_statistics": {}, "overall_github_statistics": {}}
        with patch(
            "Controllers.User.statistics_controller.GitHubService.getAllGitHubData",
            return_value=mock_data,
        ):
            response = client.get("/Dijkstra/v1/statistics/github/testuser")

        assert response.status_code == 200
        assert response.json() == mock_data

    def test_lc_returns_patched_service_response(self, client: TestClient):
        mock_data = {"leetcode": {"profile": {"username": "lcuser"}, "contestRanking": None}}
        with patch(
            "Controllers.User.statistics_controller.LeetCodeService.getAllLeetcodeData",
            return_value=mock_data,
        ):
            response = client.get("/Dijkstra/v1/statistics/lc/lcuser")

        assert response.status_code == 200
        assert response.json() == mock_data
