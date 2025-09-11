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

    GENERIC_ERROR = "GEN-ERR-000"  # Generic error code for uncategorized errors

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

    # -----------------------------
    # Opportunities → Organizations
    # -----------------------------

    # Database errors
    OPPT_ORG_DB_A01 = "OPPT-ORG-DB-A01"  # Failure inserting organization
    OPPT_ORG_DB_A02 = "OPPT-ORG-DB-A02"  # Failure updating organization
    OPPT_ORG_DB_A03 = "OPPT-ORG-DB-A03"  # Failure deleting organization

    # Server / Unexpected errors
    OPPT_ORG_SRV_A01 = "OPPT-ORG-SRV-A01"  # Generic server error
    OPPT_ORG_SRV_A02 = "OPPT-ORG-SRV-A02"  # Error fetching organizations list

    # Authentication / Permission errors
    OPPT_ORG_AUTH_A01 = "OPPT-ORG-AUTH-A01"  # User not authorized
    OPPT_ORG_AUTH_A02 = "OPPT-ORG-AUTH-A02"  # User session expired / invalid token

    # Validation / Input errors
    OPPT_ORG_VAL_A01 = "OPPT-ORG-VAL-A01"  # Invalid organization payload
    OPPT_ORG_VAL_A02 = "OPPT-ORG-VAL-A02"  # Required field missing

    # Not found errors
    OPPT_ORG_NF_A01 = "OPPT-ORG-NF-A01"  # Organization not found
