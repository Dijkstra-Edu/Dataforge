from Entities import SearchParams
from Services import CertificateGeneratorService
from Services import GitHubService

# GET Commands
async def getGitHubData(userName: str, params: SearchParams):
    if params:
        return GitHubService.getGitHubDataWithSearchParams(userName, params)
    else:
        return GitHubService.getAllGitHubData(userName)

# POST Commands
async def postDownloadCertificate(userName: str):
    return CertificateGeneratorService.mainCertificateGeneratorService(userName)
