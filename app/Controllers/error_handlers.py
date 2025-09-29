# controllers/error_handlers.py
from fastapi import Request
from Utils.error_codes import ErrorCodes
from Utils.Exceptions.opportunities_exceptions import FellowshipNotFound, InvalidTools, JobNotFound, OrganizationNotFound, ProjectOpportunityNotFound
from Utils.errors import raise_api_error
from Utils.Exceptions.user_exceptions import LocationNotFound, ProfileNotFound, UserNotFound, WorkExperienceNotFound, CertificationNotFound, CertificationUnAvailable
import logging

logger = logging.getLogger(__name__)

def register_exception_handlers(app):

    @app.exception_handler(OrganizationNotFound)
    async def org_not_found_handler(request: Request, exc: OrganizationNotFound):
        logger.warning(f"Organization not found: {exc.org_id}")
        raise_api_error(
            code=ErrorCodes.OPPT_ORG_NF_A01,
            error="Organization not found",
            detail=str(exc),
            status=404
        )

    @app.exception_handler(FellowshipNotFound)
    async def fellowship_not_found_handler(request: Request, exc: FellowshipNotFound):
        logger.warning(f"Fellowship not found: {exc.fellowship_id}")
        raise_api_error(
            code=ErrorCodes.OPPT_FEL_NF_A01,
            error="Fellowship not found",
            detail=str(exc),
            status=404
        )

    @app.exception_handler(JobNotFound)
    async def job_not_found_handler(request: Request, exc: JobNotFound):
        logger.warning(f"Job not found: {exc.job_id}")
        raise_api_error(
            code=ErrorCodes.OPPT_JOB_NF_A01,
            error="Job not found",
            detail=str(exc),
            status=404
        )

    @app.exception_handler(ProjectOpportunityNotFound)
    async def project_opportunity_not_found_handler(request: Request, exc: ProjectOpportunityNotFound):
        logger.warning(f"Project opportunity not found: {exc.project_opportunity_id}")
        raise_api_error(
            code=ErrorCodes.OPPT_PROJ_NF_A01,
            error="Project opportunity not found",
            detail=str(exc),
            status=404
        )

    @app.exception_handler(JobNotFound)
    async def job_not_found_handler(request: Request, exc: JobNotFound):
        logger.warning(f"Job not found: {exc.job_id}")
        raise_api_error(
            code=ErrorCodes.OPPT_JOB_NF_A01,
            error="Job not found",
            detail=str(exc),
            status=404
        )

    @app.exception_handler(InvalidTools)
    async def invalid_tools_handler(request: Request, exc: InvalidTools):
        logger.warning(f"Invalid {exc.field}: {exc.invalid}")
        raise_api_error(
            code=ErrorCodes.OPPT_ORG_VAL_A01,
            error="Invalid input",
            detail=str(exc),
            status=400
        )

    @app.exception_handler(UserNotFound)
    async def user_not_found_handler(request: Request, exc: UserNotFound):
        logger.warning(f"User not found: {exc.user_id}")
        raise_api_error(
            code=ErrorCodes.USER_USER_NF_A01,
            error="User not found",
            detail=str(exc),
            status=404
        )

    @app.exception_handler(ProfileNotFound)
    async def profile_not_found_handler(request: Request, exc: ProfileNotFound):
        logger.warning(f"Profile not found: {exc.profile_id}")
        raise_api_error(
            code=ErrorCodes.USER_PROFILE_NF_A01,
            error="Profile not found",
            detail=str(exc),
            status=404
        )

    @app.exception_handler(LocationNotFound)
    async def location_not_found_handler(request: Request, exc: LocationNotFound):
        logger.warning(f"Location not found: {exc.location_id}")
        raise_api_error(
            code=ErrorCodes.USER_LOCATION_NF_A01,
            error="Location not found",
            detail=str(exc),
            status=404
        )

    @app.exception_handler(WorkExperienceNotFound)
    async def work_experience_not_found_handler(request: Request, exc: WorkExperienceNotFound):
        logger.warning(f"Work experience not found: {exc.work_experience_id}")
        raise_api_error(
            code=ErrorCodes.USER_WORK_EXPERIENCE_NF_A01,
            error="Work experience not found",
            detail=str(exc),
            status=404
        )

    @app.exception_handler(CertificationNotFound)
    async def certification_not_found_handler(request: Request, exc: CertificationNotFound):
        logger.warning(f"Certificate not found: {exc.certificate_id}")
        raise_api_error(
            code=ErrorCodes.USER_CERTIFICATE_NF_A01,
            error="Certificate not found",
            detail=str(exc),
            status=404
        )

    @app.exception_handler(CertificationUnAvailable)
    async def certifications_unavailable_handler(request: Request, exc: CertificationUnAvailable):
        logger.info("No certifications available")
        raise_api_error(
            code=ErrorCodes.USER_CERTIFICATE_NF_A01,
            error="No certifications found",
            detail=str(exc),
            status=404
        )

    @app.exception_handler(Exception)
    async def generic_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled error: {str(exc)}")
        raise_api_error(
            code=ErrorCodes.GENERIC_ERROR,
            error="Internal server error",
            detail="An unexpected error occurred",
            status=500
        )
