from fastapi import APIRouter
from Settings.logging_config import get_logger
from Services.User.statistics_service import StatisticsService

# Initialize logging
logger = get_logger()

router = APIRouter(prefix="/Dijkstra/v1/statistics", tags=["Statistics"])

@router.get('/lc/{userName}')
async def getLeetCodeData(userName: str):
    logger.info("GET Request LeetCode Data for user: " + userName)
    return StatisticsService.getAllLeetcodeData(userName)