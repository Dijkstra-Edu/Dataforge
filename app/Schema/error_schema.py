# schemas/error_schema.py
from pydantic import BaseModel

class APIError(BaseModel):
    code: str           # Unique error code for programmatic handling
    error: str          # Short, human-readable error message
    detail: str         # Detailed explanation for the client
    status: int         # HTTP status code associated with the error