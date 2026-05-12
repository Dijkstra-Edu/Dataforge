from fastapi import APIRouter
from Settings.logging_config import get_logger
from Services.User.dijkstra_certificate_service import CertificateGeneratorService

# Initialize logging
logger = get_logger()

router = APIRouter(prefix="/Dijkstra/v1/certificate", tags=["Certificate"])

@router.post('/download/{userName}')
async def postDownloadCertificate(userName: str):
    logger.info("POST Request Certificate Download for user: " + userName)
    return await CertificateGeneratorService.mainCertificateGeneratorService(userName)