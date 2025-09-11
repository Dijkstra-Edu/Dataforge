# utils/error_codes.py

class ErrorCodes:
    """
    Standardized alphanumeric error codes for the API.
    Format: xxxx-yyyy-zzzz-abc
        xxxx: Subdivision (USER, OPPT)
        yyyy: Feature within subdivision (e.g., PROJ for Project Opportunities)
        zzzz: Error type (DB, SRV, AUTH, VAL, NF)
        abc: Alphanumeric error number (A01, A02, etc.)
    """

    # -----------------------------
    # Opportunities → Project Opportunities
    # -----------------------------

    # Database errors
    OPPT_PROJ_DB_A01 = "OPPT-PROJ-DB-A01"  # Failure inserting project
    OPPT_PROJ_DB_A02 = "OPPT-PROJ-DB-A02"  # Failure updating project
    OPPT_PROJ_DB_A03 = "OPPT-PROJ-DB-A03"  # Failure deleting project

    # Server / Unexpected errors
    OPPT_PROJ_SRV_A01 = "OPPT-PROJ-SRV-A01"  # Generic server error
    OPPT_PROJ_SRV_A02 = "OPPT-PROJ-SRV-A02"  # Error fetching projects list

    # Authentication / Permission errors
    OPPT_PROJ_AUTH_A01 = "OPPT-PROJ-AUTH-A01"  # User not authorized
    OPPT_PROJ_AUTH_A02 = "OPPT-PROJ-AUTH-A02"  # User session expired / invalid token

    # Validation / Input errors
    OPPT_PROJ_VAL_A01 = "OPPT-PROJ-VAL-A01"  # Invalid project payload
    OPPT_PROJ_VAL_A02 = "OPPT-PROJ-VAL-A02"  # Required field missing

    # Not found errors
    OPPT_PROJ_NF_A01 = "OPPT-PROJ-NF-A01"  # Project not found
