from fastapi import APIRouter
from Settings.logging_config import setup_logging
from Services.certificate_service import CertificateGeneratorService

# Initialize logging
logger = setup_logging()

router = APIRouter(prefix="/Dijkstra/v1/certificate", tags=["Certificate"])

@router.get('/health', status_code=200)
async def root():
    logger.info("Health Endpoint Triggered")
    return {"status": 200, 'message': 'Dijkstra Certificate Generator Health Endpoint Triggered!!!'}

@router.post('/download/{userName}')
async def postDownloadCertificate(userName: str):
    logger.info("POST Request Certificate Download for user: " + userName)
    return await CertificateGeneratorService.mainCertificateGeneratorService(userName)