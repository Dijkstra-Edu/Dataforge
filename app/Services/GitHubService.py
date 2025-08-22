import os
from typing import Dict
import httpx
import asyncio
from fastapi import HTTPException
from dotenv import load_dotenv
from pydantic import BaseModel
import requests
from Entities import SearchParams
from Settings.logging_config import setup_logging
from collections import Counter

logger = setup_logging()
load_dotenv()
GITHUB_API_URL = "https://api.github.com/graphql"
GITHUB_API = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
ORG_NAME = "Dijkstra-Edu" 

HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}" if GITHUB_TOKEN else ""
}

# -------------------- Public API --------------------

async def getAllCertData(username: str):
    return await cert_data(username)

async def getAllGitHubData(username: str):
    pass

def getGitHubDataWithSearchParams(username: str, params: SearchParams):
    pass

# -------------------- DTO --------------------

class GitHubContributions(BaseModel):
    username: str
    organization: str
    total_commits: int
    total_pull_requests: int
    total_lines_added: int

# -------------------- Internal Service --------------------

async def fetch_json(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"GitHub API error: {response.text}")
        return response.json()

async def get_org_repos(org: str):
    url = f"{GITHUB_API}/orgs/{org}/repos?per_page=100"
    return await fetch_json(url)

# TODO - This needs to be done through the API, not like this
async def count_user_contributions(username: str, org: str, params: Dict[str, bool]) -> GitHubContributions:
    async with httpx.AsyncClient() as client:
        repos = await get_org_repos(org)

        total_commits = 0
        total_pull_requests=0
        total_lines_added = 0
        

        # Process repositories concurrently
        repo_tasks = []
        for repo in repos:
            repo_name = repo['name']
            full_name = f"{org}/{repo_name}"
            repo_tasks.append(process_repo(client, full_name, username, params))

        results = await asyncio.gather(*repo_tasks, return_exceptions=True)

        for result in results:
            if not isinstance(result, Exception):
                total_commits += result['commits']
                total_pull_requests += result['pulls']
                total_lines_added += result['additions']
                

    return GitHubContributions(
        username=username,
        organization=org,
        total_commits=total_commits,
        total_pull_requests=total_pull_requests,
        total_lines_added=total_lines_added,
    )

async def process_repo(client: httpx.AsyncClient, full_name: str, username: str, params: Dict[str, bool]) -> Dict:
    result = {
        'commits': 0,
        'issues': 0,
        'additions': 0,
    }

    if params.get("commits", True):
        # Process commits
        commits_url = f"{GITHUB_API}/repos/{full_name}/commits?author={username}&per_page=100"
        commits = await fetch_json_with_client(client, commits_url)
        result['commits'] = len(commits)

        # Process commit stats concurrently
        commit_tasks = []
        for commit in commits:
            sha = commit.get("sha")
            if sha:
                commit_detail_url = f"{GITHUB_API}/repos/{full_name}/commits/{sha}"
                commit_tasks.append(get_commit_stats(client, commit_detail_url))

        commit_stats = await asyncio.gather(*commit_tasks, return_exceptions=True)
        for stats in commit_stats:
            if isinstance(stats, dict):
                result['additions'] += stats.get("additions", 0)
                

    if params.get("issues", True):
        issues_url = f"{GITHUB_API}/repos/{full_name}/issues?creator={username}&state=all&per_page=100"
        issues = await fetch_json_with_client(client, issues_url)
        result['issues'] = sum(1 for issue in issues if 'pull_request' not in issue)

    if params.get("pulls", True):
        pulls_url = f"{GITHUB_API}/repos/{full_name}/pulls?state=all&creator={username}&per_page=100"
        pulls = await fetch_json_with_client(client, pulls_url)
        result['pulls'] = len(pulls)

    return result

async def fetch_json_with_client(client: httpx.AsyncClient, url: str):
    response = await client.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"GitHub API error: {response.text}")
    return response.json()

async def get_commit_stats(client: httpx.AsyncClient, url: str):
    try:
        response = await client.get(url, headers=HEADERS)
        return response.json().get("stats", {})
    except Exception as e:
        logger.warning(f"Failed to fetch commit stats: {e}")
        return {}
    
ORG_ID_QUERY = """
query($orgLogin: String!) {     
  organization(login: $orgLogin) {
    id
  }
}
"""

# Main user data query (pullRequestReviews omitted as it's unsupported)
CERT_USER_DATA_QUERY = """
query ($userLogin: String!, $orgID: ID!) {
  user(login: $userLogin) {
    login
    name
    contributionsCollection(organizationID: $orgID) {
      startedAt
      endedAt
      contributionCalendar {
        totalContributions
      }
    }
  }
}
"""

def run_github_query(query, variables):
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    response = requests.post(GITHUB_API_URL, json={"query": query, "variables": variables}, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    result = response.json()
    if "errors" in result:
        raise HTTPException(status_code=400, detail=result["errors"])
    return result["data"]

def get_org_id(org_login: str) -> str:
    data = run_github_query(ORG_ID_QUERY, {"orgLogin": org_login})
    org = data.get("organization")
    if not org:
        raise HTTPException(status_code=404, detail=f"Organization '{org_login}' not found")
    return org["id"]

#---------------------------- ONLY CERTIFICATE DATA --------------------------------------
async def cert_data(username: str):
    org_id = get_org_id(ORG_NAME)
    data = run_github_query(CERT_USER_DATA_QUERY, {"userLogin": username, "orgID": org_id})
    user = data.get("user")
    if not user:
        raise HTTPException(status_code=404, detail=f"User '{username}' not found")

    contribs = user.get("contributionsCollection")
    if not contribs:
        return {"message": "No contributions found"}


    return {
        "login": user["login"],
        "name": user["name"],
        "startingDateOfContribution": contribs.get("startedAt"),
        "endingDateOfContribution": contribs.get("endedAt"),
    }