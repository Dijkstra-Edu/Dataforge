from uuid import UUID
from sqlmodel import Session, select
from typing import List, Optional


from Entities.UserDTOs.profile_entity import CreateProfile, UpdateProfile
from Schema.SQL.Models.models import Profile, User
from Repository.User.profile_repository import ProfileRepository
from Utils.Exceptions.user_exceptions import GitHubUsernameNotFound, ProfileAlreadyExists, ProfileNotFound, ProfileNotFound, UserNotFound

class ProfileService:
    def __init__(self, session: Session):
        self.repo = ProfileRepository(session)
        self.session = session

    def create_profile(self, profile_create: CreateProfile) -> Profile:
        # Check if user exists
        user = self.session.get(User, profile_create.user_id)
        if not user:
            raise UserNotFound(profile_create.user_id)
        
        # Check if profile already exists for this user
        existing_profile = self.repo.get_by_user_id(profile_create.user_id)
        if existing_profile:
            raise ProfileAlreadyExists(profile_create.user_id)
        
        profile = Profile(**profile_create.dict(exclude_unset=True))
        return self.repo.create(profile)

    def get_profile(self, profile_id: UUID) -> Optional[Profile]:
        profile = self.repo.get(profile_id)
        if not profile:
            return ProfileNotFound(profile_id)
        return profile

    def get_profile_by_user_id(self, user_id: UUID) -> Optional[Profile]:
        profile = self.repo.get_by_user_id(user_id)
        if not profile:
            return ProfileNotFound(user_id)
        return profile

    def get_profile_id_by_github_username(self, github_username: str) -> UUID:
        """
        Get profile ID by GitHub username.
        This is a helper method to simplify getting profile_id from github_username.
        
        Args:
            github_username: GitHub username of the user
            
        Returns:
            UUID: Profile ID
        """
        from Services.User.user_service import UserService
        
        user_service = UserService(self.session)
        user_id = user_service.get_user_id_by_github_username(github_username)
        profile = self.get_profile_by_user_id(user_id)
        return profile.id

    def list_profiles(
        self,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        order: str = "desc",
        user_id: Optional[UUID] = None,
    ) -> List[Profile]:
        """
        Supports pagination, filtering, and sorting.
        """
        return self.repo.list(
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            order=order,
            user_id=user_id,
        )

    def update_profile(self, profile_id: UUID, profile_update: UpdateProfile) -> Optional[Profile]:
        profile = self.repo.get(profile_id)
        if not profile:
            return ProfileNotFound(profile_id)

        # Check if user_id is being updated and if the new user exists
        if profile_update.user_id and profile_update.user_id != profile.user_id:
            user = self.session.get(User, profile_update.user_id)
            if not user:
                raise UserNotFound(profile_update.user_id)

            # Check if profile already exists for the new user
            existing_profile = self.repo.get_by_user_id(profile_update.user_id)
            if existing_profile:
                raise ProfileAlreadyExists(profile_update.user_id)

        update_data = profile_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(profile, key, value)
        return self.repo.update(profile)

    def delete_profile(self, profile_id: UUID) -> Optional[str]:
        profile = self.repo.get(profile_id)
        if not profile:
            return ProfileNotFound(profile_id)
        self.repo.delete(profile)
        return f"Profile with ID {profile_id} deleted successfully."

    # Secondary Methods
    def get_profile_with_user_details(self, profile_id: UUID) -> Optional[Profile]:
        profile = self.repo.get_with_user_details(profile_id)
        if profile:
            # This will load the user relationship if it's not already loaded
            # You might need to adjust this based on your actual relationship setup
            return profile
        return None


    def get_profile_full_data_by_user_id(self, user_id: UUID) -> dict:
        """
        Get full profile data with all nested relationships populated.
        Returns profile with education, work experience, certifications, 
        publications, volunteering, projects, and leetcode (None for now).
        """
        from Services.User.education_service import EducationService
        from Services.User.workexperience_service import WorkExperienceService
        from Services.User.certifications_service import CertificationService
        from Services.User.publication_service import PublicationService
        from Services.User.volunteering_service import VolunteeringService
        from Services.User.projects_service import ProjectsService
        from Entities.UserDTOs.profile_entity import ReadProfile
        from Entities.UserDTOs.certification_entity import ReadCertification
        from Entities.UserDTOs.publication_entity import ReadPublication
        from Entities.UserDTOs.volunteering_entity import ReadVolunteering
        from Entities.UserDTOs.projects_entity import ReadProject
        
        # Get the base profile
        profile = self.get_profile_by_user_id(user_id)
        profile_dict = ReadProfile.model_validate(profile).model_dump()
        
        # Initialize all sub-services
        education_service = EducationService(self.session)
        work_exp_service = WorkExperienceService(self.session)
        cert_service = CertificationService(self.session)
        pub_service = PublicationService(self.session)
        vol_service = VolunteeringService(self.session)
        proj_service = ProjectsService(self.session)
        
        # Get all related data
        profile_dict['education'] = education_service.get_educations_by_profile_with_locations(profile.id)
        profile_dict['work_experience'] = work_exp_service.get_work_experiences_by_profile_with_locations(profile.id)
        
        # Get certifications
        try:
            certifications = cert_service.get_certifications_by_profile(profile.id)
            profile_dict['certifications'] = [ReadCertification.model_validate(cert).model_dump() for cert in certifications]
        except:
            profile_dict['certifications'] = []
        
        # Get publications
        try:
            publications = pub_service.get_publications_by_profile_id(profile.id)
            profile_dict['publications'] = [ReadPublication.model_validate(pub).model_dump() for pub in publications]
        except:
            profile_dict['publications'] = []
        
        # Get volunteering
        try:
            volunteering = vol_service.get_volunteering_by_profile_id(profile.id)
            profile_dict['volunteering'] = [ReadVolunteering.model_validate(vol).model_dump() for vol in volunteering]
        except:
            profile_dict['volunteering'] = []
        
        # Get projects
        try:
            projects = proj_service.get_projects_by_profile(profile.id)
            profile_dict['projects'] = [proj.model_dump() if hasattr(proj, 'model_dump') else proj for proj in projects]
        except:
            profile_dict['projects'] = []
        
        # Leetcode excluded for now
        profile_dict['leetcode'] = None
        
        return profile_dict

    
    def get_profile_full_data_by_github_username(self, github_username: str) -> dict:
        """
        Get full profile data by GitHub username.
        This method looks up the user by GitHub username, then calls 
        get_profile_full_data_by_user_id to retrieve the full profile data,
        and adds GitHub data to the response.
        
        Args:
            github_username: GitHub username of the user
            
        Returns:
            dict: Full profile data with all nested relationships
        """
        from Services.User.user_service import UserService
        
        # Get user by GitHub username
        user_service = UserService(self.session)
        user_id = user_service.get_user_id_by_github_username(github_username)

        print("TestUser:", user_id)
        
        # Call the existing method with user_id
        return self.get_profile_full_data_by_user_id(user_id)