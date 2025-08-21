from fastapi import APIRouter
from Settings.logging_config import setup_logging

# Initialize logging
logger = setup_logging()

router = APIRouter(prefix="/Dijkstra/v1", tags=["Main Controller"])

@router.get('/health', status_code=200)
async def root():
    logger.info("Health Endpoint Triggered")
    return {"status": 200, 'message': 'Dijkstra Server Health Endpoint Triggered!!!'}