import os
from typing import Dict
import os
from typing import Dict, Any
from dotenv import load_dotenv
from Settings.logging_config import setup_logging

logger = setup_logging()
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}" if GITHUB_TOKEN else ""
}

class GitHubService:
  @staticmethod
  def getAllGitHubData(username: str) -> Dict[str, Any]:
    
#   General Data
# - UserName
# - Full Name
# - Avatar Img Link
# - Bio
# - Followers
# - Following
# - Current Company
# - Current Location
# - Time Zone
# - Websites/Links
# - Organizations List

# Dijkstra Specific Statistics
# - Team (List of Objects)
#      - Team Name
#      - Team Link
#      - Superior
# - Repositories Contributed to (List) - Repository list (all of these stats need to be specific to Repo within Dijkstra)
#     - Lines Added
#     - Lines Removed
#     - Frameworks present in Repo (We assume that this is what the user has worked with)
#     - Languages Used (By User) : List
#          - Language Name
#          - Language Percentage Used
#          - Total Lines contributed with said Language
#     - PR's raised
#     - Commits
#     - Issues Created
# - Total PR's
# - Total Lines contributed
# - Total Commits
# - Total Issues Created
# - Start Date
# - Time Period (Start Date to Last Contribution)
# - Dijkstra Rank (Say Gold)
# - Repositories Forked

# Overall GitHub Statistics
# - Total Lines Contributed
# - Total PR's raised
# - Total Issues Created
# - Total Repos (forked/private)
# - Total Commits
# - Languages Used (By User) : List
#          - Language Name
#          - Language Percentage Used
#          - Total Lines contributed with said Language
# - Contribution Graph Link

    return {
      "general_data": {
          "username": "johndoe",
          "full_name": "John Doe",
          "avatar_img_link": "https://avatars.githubusercontent.com/u/123456?v=4",
          "bio": "Software engineer passionate about open source and education.",
          "followers": 150,
          "following": 45,
          "current_company": "Dijkstra",
          "current_location": "Zurich, Switzerland",
          "time_zone": "CET",
          "websites_links": ["https://johndoe.dev", "https://github.com/johndoe"],
          "organizations_list": ["Dijkstra", "Python Software Foundation"]
      },
      "dijkstra_statistics": {
          "team": [
              {
                  "team_name": "Backend Wizards",
                  "team_link": "https://github.com/orgs/Dijkstra/teams/backend-wizards",
                  "superior": "Alice Smith"
              },
              {
                  "team_name": "Frontend Ninjas",
                  "team_link": "https://github.com/orgs/Dijkstra/teams/frontend-ninjas",
                  "superior": "Bob Johnson"
              }
          ],
          "repositories_contributed_to": [
              {
                  "repo_name": "dijkstra-core",
                  "lines_added": 1200,
                  "lines_removed": 300,
                  "frameworks_present": ["FastAPI", "React"],
                  "languages_used": [
                      {"language_name": "Python", "percentage_used": 70, "total_lines": 840},
                      {"language_name": "TypeScript", "percentage_used": 30, "total_lines": 360}
                  ],
                  "prs_raised": 10,
                  "commits": 25,
                  "issues_created": 5
              },
              {
                  "repo_name": "dijkstra-frontend",
                  "lines_added": 800,
                  "lines_removed": 200,
                  "frameworks_present": ["Next.js", "TailwindCSS"],
                  "languages_used": [
                      {"language_name": "TypeScript", "percentage_used": 90, "total_lines": 720},
                      {"language_name": "CSS", "percentage_used": 10, "total_lines": 80}
                  ],
                  "prs_raised": 7,
                  "commits": 18,
                  "issues_created": 3
              }
          ],
          "total_prs": 17,
          "total_lines_contributed": 2500,
          "total_commits": 43,
          "total_issues_created": 8,
          "start_date": "2023-01-15",
          "time_period": "2023-01-15 to 2025-08-13",
          "dijkstra_rank": "Gold",
          "repositories_forked": ["dijkstra-utils", "dijkstra-docs"]
      },
      "overall_github_statistics": {
          "total_lines_contributed": 10000,
          "total_prs_raised": 75,
          "total_issues_created": 20,
          "total_repos": 30,
          "total_commits": 150,
          "languages_used": [
              {"language_name": "Python", "percentage_used": 60, "total_lines": 6000},
              {"language_name": "TypeScript", "percentage_used": 30, "total_lines": 3000},
              {"language_name": "CSS", "percentage_used": 10, "total_lines": 1000}
          ],
          "contribution_graph_link": "https://github.com/johndoe"
      }
  }


