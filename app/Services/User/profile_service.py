from uuid import UUID
from fastapi import Depends
from kafka import KafkaProducer
from sqlmodel import Session, select
from typing import List, Optional


from Entities.UserDTOs.profile_entity import CreateProfile, ReadProfile, UpdateProfile
from Schema.SQL.Models.models import Profile, User
from Repository.User.profile_repository import ProfileRepository
from Utils.Exceptions.user_exceptions import GitHubUsernameNotFound, ProfileAlreadyExists, ProfileNotFound, ProfileNotFound
from Utils.Exceptions.user_exceptions import ProfileAlreadyExists, ProfileNotFound, ProfileNotFound, UserNotFound

from Entities.UserDTOs.profile_entity_kafka_dto import map_profile_to_kafka_event
from Services.Kafka.producer_service import KafkaProducerService, get_kafka_producer
from db import get_session

class ProfileService:
    def __init__(self, session: Session, kafka_producer: KafkaProducerService = None):
        self.repo = ProfileRepository(session)
        self.session = session
        self.kafka_producer = kafka_producer

    def create_profile(self, profile_create: CreateProfile) -> Profile:
        user = self.session.exec(
            select(User).where(User.github_user_name == profile_create.username)
        ).first()
        if not user:
            raise GitHubUsernameNotFound(profile_create.username)

        existing_profile = self.repo.get_by_username(profile_create.username)
        if existing_profile:
            raise ProfileAlreadyExists(profile_create.username)

        profile = Profile(username=profile_create.username)
        return self.repo.create(profile)

    def get_profile(self, profile_id: UUID) -> Optional[Profile]:
        profile = self.repo.get(profile_id)
        if not profile:
            raise ProfileNotFound(profile_id)
        return profile

    def get_profile_by_user_id(self, user_id: UUID) -> Optional[Profile]:
        profile = self.repo.get_by_user_id(user_id)
        if not profile:
            raise ProfileNotFound(user_id)
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
        profile = self.repo.get_by_username(github_username)
        if not profile:
            raise ProfileNotFound(github_username)
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
            raise ProfileNotFound(profile_id)

        update_data = profile_update.dict(exclude_unset=True)
        new_username = update_data.get("username")
        if new_username is not None and new_username != profile.username:
            user = self.session.exec(
                select(User).where(User.github_user_name == new_username)
            ).first()
            if not user:
                raise GitHubUsernameNotFound(new_username)
            other = self.repo.get_by_username(new_username)
            if other and other.id != profile_id:
                raise ProfileAlreadyExists(new_username)

        for key, value in update_data.items():
            setattr(profile, key, value)
        return self.repo.update(profile)

    def delete_profile(self, profile_id: UUID) -> Optional[str]:
        profile = self.repo.get(profile_id)
        if not profile:
            raise ProfileNotFound(profile_id)
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


    def get_profile_by_profile_id(self, profile_id: UUID) -> Profile:
        """
        Get full profile data with all nested relationships populated.
        Returns profile with education, work experience, certifications, 
        publications, volunteering, projects, and leetcode (None for now).
        """
        
        # Get the base profile
        from Entities.UserDTOs.profile_entity import ReadProfile
        profile = self.get_profile(profile_id)
        return profile
    
    def populate_full_profile_data(self, profile: Profile, fields: list[str] | str = "all") -> dict:
        """
        Populate full profile data with selected nested relationships.
        
        Args:
            profile (Profile): Base profile object.
            fields (list[str] | str): Sections to fetch. 
                                    Use "all" (default) to fetch everything.
                                    Example: ["education", "projects", "certifications"]

        Returns:
            dict: Profile dictionary with selected nested relations populated.
        """

        # If user passed "all" or omitted fields → fetch everything
        fetch_all = fields == "all"
        if not fetch_all and not isinstance(fields, list):
            raise ValueError("fields must be 'all' or a list of field names")

        # Local import to avoid circular dependencies
        from Services.User.education_service import EducationService
        from Services.User.workexperience_service import WorkExperienceService
        from Services.User.certifications_service import CertificationService
        from Services.User.publication_service import PublicationService
        from Services.User.volunteering_service import VolunteeringService
        from Services.User.projects_service import ProjectsService

        from Entities.UserDTOs.certification_entity import ReadCertification
        from Entities.UserDTOs.publication_entity import ReadPublication
        from Entities.UserDTOs.volunteering_entity import ReadVolunteering

        profile_id = profile.id
        # Initialize sub-services (only once)
        education_service = EducationService(self.session)
        work_exp_service = WorkExperienceService(self.session)
        cert_service = CertificationService(self.session)
        pub_service = PublicationService(self.session)
        vol_service = VolunteeringService(self.session)
        proj_service = ProjectsService(self.session)
        profile_dict = ReadProfile.model_validate(profile).model_dump()
        # Helper to check whether a field needs to be fetched
        def need(field_name: str) -> bool:
            return fetch_all or field_name in fields

        # -------------------------------
        # Conditional population
        # -------------------------------
        if need("education"):
            profile_dict["education"] = education_service.get_educations_by_profile_with_locations(profile_id)

        if need("work_experience"):
            profile_dict["work_experience"] = work_exp_service.get_work_experiences_by_profile_with_locations(profile_id)

        if need("certifications"):
            try:
                certifications = cert_service.get_certifications_by_profile(profile_id)
                profile_dict["certifications"] = [
                    ReadCertification.model_validate(cert).model_dump() for cert in certifications
                ]
            except Exception:
                profile_dict["certifications"] = []

        if need("publications"):
            try:
                publications = pub_service.get_publications_by_profile_id(profile_id)
                profile_dict["publications"] = [
                    ReadPublication.model_validate(pub).model_dump() for pub in publications
                ]
            except Exception:
                profile_dict["publications"] = []

        if need("volunteering"):
            try:
                vols = vol_service.get_volunteering_by_profile_id(profile_id)
                profile_dict["volunteering"] = [
                    ReadVolunteering.model_validate(vol).model_dump() for vol in vols
                ]
            except Exception:
                profile_dict["volunteering"] = []

        if need("projects"):
            try:
                projects = proj_service.get_projects_by_profile(profile_id)
                # Some DTOs use model_dump, others do not
                profile_dict["projects"] = [
                    proj.model_dump() if hasattr(proj, "model_dump") else proj for proj in projects
                ]
            except Exception:
                profile_dict["projects"] = []

        # Leetcode (placeholder)
        if need("leetcode"):
            profile_dict["leetcode"] = None

        return profile_dict
    
    def get_profile_full_data_by_user_id(self, user_id: UUID) -> dict:
        """
        Get full profile data with all nested relationships populated.
        Returns profile with education, work experience, certifications, 
        publications, volunteering, projects, and leetcode (None for now).
        """
        from Entities.UserDTOs.profile_entity import ReadProfile
        # Get the base profile
        profile = self.get_profile_by_user_id(user_id)        
        return self.populate_full_profile_data(profile)

    
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
        return self.get_profile_full_data_by_user_id(user_id)

    def update_profile_by_github_username(self, github_username: str, profile_update: UpdateProfile) -> Profile:
        """
        Update profile by GitHub username.
        Resolves GitHub username to user_id, then to profile_id, then updates.
        """
        from Services.User.user_service import UserService
        
        # Get user by GitHub username to validate it exists and get user_id
        user_service = UserService(self.session)
        user_id = user_service.get_user_id_by_github_username(github_username)
        
        # Get profile by user_id to get profile_id
        profile = self.get_profile_by_user_id(user_id)
        
        # Update the profile using the existing method
        return self.update_profile(profile.id, profile_update)

    def delete_profile_by_github_username(self, github_username: str) -> str:
        """
        Delete profile by GitHub username.
        Resolves GitHub username to user_id, then to profile_id, then deletes.
        """
        from Services.User.user_service import UserService
        
        # Get user by GitHub username to validate it exists and get user_id
        user_service = UserService(self.session)
        user_id = user_service.get_user_id_by_github_username(github_username)
        
        # Get profile by user_id to get profile_id
        profile = self.get_profile_by_user_id(user_id)
        
        # Delete the profile using the existing method
        return self.delete_profile(profile.id)
    
    def publish_profile_update(self, profile_id: UUID):
        """
        Publish profile update event.
        This is a placeholder for the actual implementation of publishing
        profile updates to a message broker or notification system.
        """
        profile = self.get_profile_by_profile_id(profile_id)
        event = {
            "eventType": "DataForgeUpdateEvent",
            "data": map_profile_to_kafka_event(profile).model_dump(),
        }
        try:
            self.kafka_producer.publish("dm_user_metrics", key=str(profile.user_rel.github_user_name), value=event)
        except Exception as ex:
            # Production: log and/or use DLQ
            print(f"Kafka publish failed: {ex}")
            raise


def get_profile_service_with_publisher(
    session: Session = Depends(get_session),
    kafka: KafkaProducerService = Depends(get_kafka_producer),
):
    return ProfileService(session=session, kafka_producer=kafka)