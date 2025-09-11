# controllers/error_handlers.py
from fastapi import Request
from Utils.error_codes import ErrorCodes
from Utils.Exceptions.opportunities_exceptions import InvalidTools, OrganizationNotFound
from Utils.errors import raise_api_error
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

    @app.exception_handler(InvalidTools)
    async def invalid_tools_handler(request: Request, exc: InvalidTools):
        logger.warning(f"Invalid {exc.field}: {exc.invalid}")
        raise_api_error(
            code=ErrorCodes.OPPT_ORG_VAL_A01,
            error="Invalid input",
            detail=str(exc),
            status=400
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
