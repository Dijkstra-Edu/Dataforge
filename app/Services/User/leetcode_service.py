import requests
from typing import Dict, Any
from Settings.logging_config import setup_logging

from Config.constants import LEETCODE_API
from Config.queries import lc_query


logger = setup_logging()

class LeetCodeService:
    @staticmethod
    def getAllLeetcodeData(userName: str) -> Dict[str, Any]:        
        try:
            response = requests.post(
                LEETCODE_API,
                json={"query": lc_query, "variables": {"username": userName}},
                timeout=20
            )
            data = response.json()

            if "errors" in data:
                return {"leetcode": {"error": data["errors"]}}

            result_data = data.get("data", {})

            return {
                "leetcode": {
                    "profile": result_data.get("matchedUser"),
                    "contestRanking": result_data.get("userContestRanking"),
                    # "contestHistory": result_data.get("userContestRankingHistory")
                }
            }

        except Exception as e:
            return {"leetcode": {"error": str(e)}}