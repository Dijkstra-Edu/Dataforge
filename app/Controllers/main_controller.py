from fastapi import APIRouter
from Settings.logging_config import get_logger

# Initialize logging
logger = get_logger()

router = APIRouter(prefix="/Dijkstra/v1", tags=["Main Controller"])

@router.get('/health', status_code=200)
async def root():
    logger.info("Health Endpoint Triggered")
    return {"status": 200, 'message': 'Dijkstra Server Health Endpoint Triggered!!!'}