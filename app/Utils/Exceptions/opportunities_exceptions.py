# Utils/Exceptions/opportunities_exceptions.py

class ServiceError(Exception):
    """Base service exception"""

class OrganizationNotFound(ServiceError):
    def __init__(self, org_id):
        super().__init__(f"Organization with ID {org_id} does not exist.")
        self.org_id = org_id

class FellowshipNotFound(ServiceError):
    def __init__(self, fellowship_id):
        super().__init__(f"Fellowship with ID {fellowship_id} does not exist.")
        self.fellowship_id = fellowship_id

class ProjectOpportunityNotFound(ServiceError):
    def __init__(self, project_opportunity_id):
        super().__init__(f"Project Opportunity with ID {project_opportunity_id} does not exist.")
        self.project_opportunity_id = project_opportunity_id

class JobNotFound(ServiceError):
    def __init__(self, job_id):
        super().__init__(f"Job with ID {job_id} does not exist.")
        self.job_id = job_id

class InvalidTools(ServiceError):
    def __init__(self, invalid, field, allowed):
        super().__init__(f"Invalid {field}: {invalid}. Must be one of {allowed}")
        self.invalid = invalid
        self.field = field
        self.allowed = allowed
