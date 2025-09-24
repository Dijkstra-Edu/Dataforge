# Utils/Exceptions/user_exceptions.py

class ServiceError(Exception):
    """Base service exception"""

class UserNotFound(ServiceError):
    def __init__(self, user_id):
        super().__init__(f"User with ID {user_id} does not exist.")
        self.user_id = user_id

class ProfileNotFound(ServiceError):
    def __init__(self, profile_id):
        super().__init__(f"Profile with ID {profile_id} does not exist.")
        self.profile_id = profile_id

class ProfileAlreadyExists(ServiceError):
    def __init__(self, user_id):
        super().__init__(f"Profile already exists for user ID {user_id}.")
        self.user_id = user_id

class LocationNotFound(ServiceError):
    def __init__(self, location_id):
        super().__init__(f"Location with ID {location_id} does not exist.")
        self.location_id = location_id

class WorkExperienceNotFound(ServiceError):
    def __init__(self, work_experience_id):
        super().__init__(f"Work Experience with ID {work_experience_id} does not exist.")
        self.work_experience_id = work_experience_id

class GitHubUsernameNotFound(ServiceError):
    def __init__(self, github_username):
        super().__init__(f"User with GitHub username '{github_username}' does not exist.")
        self.github_username = github_username

class GitHubUsernameAlreadyExists(ServiceError):
    def __init__(self, github_username):
        super().__init__(f"User with GitHub username '{github_username}' already exists.")
        self.github_username = github_username

class VolunteeringNotFound(ServiceError):
    def __init__(self, volunteering_id):
        super().__init__(f"Volunteering entry with ID {volunteering_id} does not exist.")
        self.volunteering_id = volunteering_id

class PublicationNotFound(ServiceError):
    def __init__(self, publication_id):
        super().__init__(f"Publication with ID {publication_id} does not exist.")
        self.publication_id = publication_id
