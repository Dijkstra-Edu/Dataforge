"""Unit tests for LeetCodeService.getAllLeetcodeData (statistics)."""
import pytest
from unittest.mock import patch, MagicMock

from Services.User.leetcode_service import LeetCodeService


@pytest.mark.unit
class TestLeetCodeServiceGetAllLeetcodeData:
    """Tests for LeetCodeService.getAllLeetcodeData."""

    def test_returns_leetcode_profile_and_contest_ranking_on_success(self):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {
                "matchedUser": {"username": "testuser", "profile": {}},
                "userContestRanking": {"rating": 1500},
            }
        }
        mock_response.raise_for_status = MagicMock()

        with patch(
            "Services.User.leetcode_service.requests.post",
            return_value=mock_response,
        ):
            result = LeetCodeService.getAllLeetcodeData("testuser")

        assert "leetcode" in result
        assert result["leetcode"]["profile"] == {"username": "testuser", "profile": {}}
        assert result["leetcode"]["contestRanking"] == {"rating": 1500}
        assert "error" not in result

    def test_returns_leetcode_error_when_api_returns_errors_key(self):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "errors": [{"message": "User not found"}]
        }

        with patch(
            "Services.User.leetcode_service.requests.post",
            return_value=mock_response,
        ):
            result = LeetCodeService.getAllLeetcodeData("nonexistent")

        assert "leetcode" in result
        assert "error" in result["leetcode"]
        assert result["leetcode"]["error"] == [{"message": "User not found"}]

    def test_returns_error_key_on_request_exception(self):
        with patch(
            "Services.User.leetcode_service.requests.post",
            side_effect=Exception("Connection failed"),
        ):
            result = LeetCodeService.getAllLeetcodeData("anyuser")

        assert "error" in result
        assert "Connection failed" in result["error"]
