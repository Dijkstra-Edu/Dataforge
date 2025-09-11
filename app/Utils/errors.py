# utils/errors.py
from turtle import title
from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from Schema.error_schema import APIError

def raise_api_error(
    code: str,
    error: str,
    detail: str,
    status: int = HTTP_500_INTERNAL_SERVER_ERROR
):
    error = APIError(code=code, error=error, detail=detail, status=status)
    raise HTTPException(status_code=status, detail=error.dict())
