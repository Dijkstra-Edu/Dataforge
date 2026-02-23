from fastapi import APIRouter
from Settings.logging_config import setup_logging
from Services.User.github_service import GitHubService
from Services.User.leetcode_service import LeetCodeService

# Initialize logging
logger = setup_logging()

router = APIRouter(prefix="/Dijkstra/v1/statistics", tags=["Statistics"])

@router.get('/health', status_code=200)
async def root():
    logger.info("Health Endpoint Triggered")
    return {"status": 200, 'message': 'Dijkstra Statistics Health Endpoint Triggered!!!'}

@router.get('/github/{userName}')
async def getGitHubData(userName: str):
    logger.info("GET Request GitHub Data for user: " + userName)
    return await GitHubService.getAllGitHubData(userName)

@router.get('/lc/{userName}')
async def getLeetCodeData(userName: str):
    logger.info("GET Request LeetCode Data for user: " + userName)
    return await LeetCodeService.getAllLeetcodeData(userName)