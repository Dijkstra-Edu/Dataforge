# Utils/Exceptions/opportunities_exceptions.py

class ServiceError(Exception):
    """Base service exception"""

class OrganizationNotFound(ServiceError):
    def __init__(self, org_id):
        super().__init__(f"Organization with ID {org_id} does not exist.")
        self.org_id = org_id

class InvalidTools(ServiceError):
    def __init__(self, invalid, field, allowed):
        super().__init__(f"Invalid {field}: {invalid}. Must be one of {allowed}")
        self.invalid = invalid
        self.field = field
        self.allowed = allowed
