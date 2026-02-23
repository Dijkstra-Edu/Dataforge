"""Unit tests for GitHubService (statistics)."""
import pytest

from Services.User.github_service import GitHubService


@pytest.mark.unit
class TestGitHubService:
    """Tests for GitHubService.getAllGitHubData."""

    def test_get_all_github_data_returns_dict_with_expected_top_level_keys(self):
        result = GitHubService.getAllGitHubData("johndoe")
        assert isinstance(result, dict)
        assert "general_data" in result
        assert "dijkstra_statistics" in result
        assert "overall_github_statistics" in result

    def test_get_all_github_data_general_data_structure(self):
        result = GitHubService.getAllGitHubData("anyuser")
        general = result["general_data"]
        assert "username" in general
        assert "full_name" in general
        assert "avatar_img_link" in general
        assert "bio" in general
        assert "followers" in general
        assert "following" in general
        assert "current_company" in general
        assert "current_location" in general
        assert "time_zone" in general
        assert "websites_links" in general
        assert "organizations_list" in general

    def test_get_all_github_data_dijkstra_statistics_structure(self):
        result = GitHubService.getAllGitHubData("anyuser")
        dijkstra = result["dijkstra_statistics"]
        assert "team" in dijkstra
        assert "repositories_contributed_to" in dijkstra
        assert "total_prs" in dijkstra
        assert "total_lines_contributed" in dijkstra
        assert "total_commits" in dijkstra
        assert "dijkstra_rank" in dijkstra

    def test_get_all_github_data_overall_statistics_structure(self):
        result = GitHubService.getAllGitHubData("anyuser")
        overall = result["overall_github_statistics"]
        assert "total_lines_contributed" in overall
        assert "total_prs_raised" in overall
        assert "total_commits" in overall
        assert "languages_used" in overall
        assert "contribution_graph_link" in overall
