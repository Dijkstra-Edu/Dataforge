# Services/users_service.py

from uuid import UUID
from typing import List, Optional
from sqlmodel import Session
from Repository.User.user_repository import UserRepository
from Repository.User.profile_repository import ProfileRepository
from Repository.User.links_repository import LinksRepository
from Services.User.location_service import LocationService
from Entities.UserDTOs.user_entity import CreateUser, ReadUserAuthDetails, ReadUserPersonalDetails, UpdateUser, OnboardUser, OnboardCheckResponse, ReadUserCardDetails, UpdateUserPersonalDetails
from Schema.SQL.Models.models import User, Profile, Links, Location
from Utils.Exceptions.user_exceptions import GitHubUsernameAlreadyExists, GitHubUsernameNotFound, ProfileNotFound, UserNotFound
from Entities.UserDTOs.location_entity import UpdateLocation, CreateLocation


class UserService:
    def __init__(self, session: Session):
        self.repo = UserRepository(session)
        self.profile_repo = ProfileRepository(session)
        self.links_repo = LinksRepository(session)
        self.location_service = LocationService(session)
        self.session = session

    def create_user(self, user_create: CreateUser) -> User:
        # Check if github username already exists
        existing_user = self.repo.get_by_github_username(user_create.github_user_name)
        if existing_user:
            raise GitHubUsernameAlreadyExists(user_create.github_user_name)
        
        user = User(**user_create.dict(exclude_unset=True))
        return self.repo.create(user)

    def get_user(self, user_id: UUID) -> Optional[User]:
        user = self.repo.get(user_id)
        if not user:
            raise UserNotFound(user_id)
        return user

    def get_user_by_github_username(self, github_user_name: str) -> Optional[User]:
        user = self.repo.get_by_github_username(github_user_name)
        if not user:
            raise GitHubUsernameNotFound(github_user_name)
        return user

    def get_user_id_by_github_username(self, github_user_name: str) -> Optional[UUID]:
        user = self.repo.get_by_github_username(github_user_name)
        if not user:
            raise GitHubUsernameNotFound(github_user_name)
        return user.id

    def list_users(
        self,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        order: str = "desc",
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        github_user_name: Optional[str] = None,
        rank: Optional[str] = None,
        min_streak: Optional[int] = None,
        max_streak: Optional[int] = None,
    ) -> List[User]:
        """
        Supports pagination, filtering, and sorting.
        """
        return self.repo.list(
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            order=order,
            first_name=first_name,
            last_name=last_name,
            github_user_name=github_user_name,
            rank=rank,
            min_streak=min_streak,
            max_streak=max_streak,
        )

    def autocomplete_users(
        self,
        query: str,
        field: str = "github_user_name",
        limit: int = 10,
    ) -> List[User]:
        """
        Returns users where the given field starts with or contains query text.
        """
        return self.repo.autocomplete(query=query, field=field, limit=limit)

    def update_user(self, user_id: UUID, user_update: UpdateUser) -> Optional[User]:
        user = self.repo.get(user_id)
        if not user:
            return UserNotFound(user_id)
        
        # Check if github username is being updated and if it already exists
        if user_update.github_user_name and user_update.github_user_name != user.github_user_name:
            existing_user = self.repo.get_by_github_username(user_update.github_user_name)
            if existing_user:
                raise GitHubUsernameAlreadyExists(user_update.github_user_name)
        
        update_data = user_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        return self.repo.update(user)

    def delete_user(self, user_id: UUID) -> Optional[str]:
        user = self.repo.get(user_id)
        if not user:
            return UserNotFound(user_id)
        self.repo.delete(user)
        return f"User {user_id} deleted successfully"

    def check_onboarding_status(self, github_user_name: str) -> OnboardCheckResponse:
        """
        Check if a user has completed onboarding by github username.
        Returns OnboardCheckResponse with onboarded status and user_id if found.
        """
        onboarded, user_id = self.repo.check_onboarding_by_github_username(github_user_name)
        return OnboardCheckResponse(onboarded=onboarded, user_id=user_id)

    def onboard_user(self, onboard_data: OnboardUser) -> User:
        """
        Create a new user with onboarding_complete=True, an empty Profile, and Links.
        This is an atomic operation - User, Profile, and Links are created together.
        """
        # Check if github username already exists
        existing_user = self.repo.get_by_github_username(onboard_data.github_user_name)
        if existing_user:
            raise GitHubUsernameAlreadyExists(onboard_data.github_user_name)
        
        try:
            # Create user with onboarding_complete=True
            user_dict = onboard_data.dict(exclude_unset=True, exclude={'linkedin_user_name', 'leetcode_user_name', 'primary_email'})
            user_dict['onboarding_complete'] = True
            user_dict['data_loaded'] = False
            user = User(**user_dict)
            
            # Create user in database
            created_user = self.repo.create(user)
            
            # Create empty profile for the user
            profile = Profile(user_id=created_user.id)
            self.profile_repo.create(profile)
            
            # Create links for the user with auto-generated URLs and primary_email
            links = Links(
                user_id=created_user.id,
                github_user_name=onboard_data.github_user_name,
                github_link=f"https://github.com/{onboard_data.github_user_name}",
                linkedin_user_name=onboard_data.linkedin_user_name,
                linkedin_link=f"https://www.linkedin.com/in/{onboard_data.linkedin_user_name}",
                leetcode_user_name=onboard_data.leetcode_user_name,
                leetcode_link=f"https://leetcode.com/u/{onboard_data.leetcode_user_name}",
                primary_email=onboard_data.primary_email,
            )
            self.links_repo.create(links)
            
            # Refresh to get the updated user with relationships
            self.session.refresh(created_user)
            
            return created_user
        except Exception as e:
            # If anything fails, rollback will happen in repository layer
            raise

    def get_user_data_by_user_id(self, user_id: UUID, full_data: bool = False):
        """
        Get user data by user ID.
        If full_data=True, returns user with all nested relationships (links, profile with all sub-entities).
        If full_data=False, returns basic user data only.
        """
        from Services.User.profile_service import ProfileService
        from Entities.UserDTOs.user_entity import ReadUser
        from Entities.UserDTOs.extended_entities import ReadUserFull
        from Entities.UserDTOs.links_entity import ReadLinks
        
        # Get the base user
        user = self.get_user(user_id)
        
        if not full_data:
            # Return basic user data
            return ReadUser.model_validate(user)
        
        # Get full data
        user_dict = ReadUser.model_validate(user).model_dump()
        
        # Get links
        try:
            links = self.links_repo.get_by_user_id(user.id)
            user_dict['links'] = ReadLinks.model_validate(links).model_dump() if links else None
        except:
            user_dict['links'] = None
        
        # Get full profile data
        try:
            profile_service = ProfileService(self.session)
            user_dict['profile'] = profile_service.get_profile_full_data_by_user_id(user.id)
        except:
            user_dict['profile'] = None
        
        return user_dict

    def get_user_data_by_github_username(self, github_user_name: str, full_data: bool = False):
        """
        Get user data by GitHub username.
        If full_data=True, returns user with all nested relationships (links, profile with all sub-entities).
        If full_data=False, returns basic user data only.
        """
        from Services.User.profile_service import ProfileService
        from Entities.UserDTOs.user_entity import ReadUser
        from Entities.UserDTOs.extended_entities import ReadUserFull
        from Entities.UserDTOs.links_entity import ReadLinks
        
        # Get the base user
        user = self.get_user_by_github_username(github_user_name)
        
        if not full_data:
            # Return basic user data
            return ReadUser.model_validate(user)
        
        # Get full data
        user_dict = ReadUser.model_validate(user).model_dump()
        
        # Get links
        try:
            links = self.links_repo.get_by_user_id(user.id)
            user_dict['links'] = ReadLinks.model_validate(links).model_dump() if links else None
        except:
            user_dict['links'] = None
        
        # Get full profile data
        try:
            profile_service = ProfileService(self.session)
            user_dict['profile'] = profile_service.get_profile_full_data_by_user_id(user.id)
        except:
            user_dict['profile'] = None
        
        return user_dict

    def get_user_card_details_by_github_username(self, github_user_name: str) -> ReadUserCardDetails:
        """
        Get user card details by GitHub username.
        Returns user card details including:
        - GitHub username
        - First name
        - Middle name
        - Last name
        - Bio
        - Rank
        - Streak
        - Primary specialization
        - Secondary specializations
        - Expected salary bucket
        - LinkedIn Link
        - Personal Website Link
        - Leetcode Link
        - Time Left
        """
        # Get user by GitHub username
        user = self.get_user_by_github_username(github_user_name)
        
        # Get associated links
        links = None
        try:
            links = self.links_repo.get_by_user_id(user.id)
        except:
            # Links might not exist, continue with None
            pass
        
        # Build and return ReadUserCardDetails DTO
        return ReadUserCardDetails(
            github_user_name=user.github_user_name,
            first_name=user.first_name,
            middle_name=user.middle_name,
            last_name=user.last_name,
            bio=user.bio,
            rank=user.rank,
            streak=user.streak,
            primary_specialization=user.primary_specialization,
            secondary_specializations=user.secondary_specializations,
            expected_salary_bucket=user.expected_salary_bucket,
            time_left=user.time_left,
            linkedin_link=links.linkedin_link if links else None,
            portfolio_link=links.portfolio_link if links else None,
            leetcode_link=links.leetcode_link if links else None,
        )

    def get_user_personal_details_by_github_username(self, github_user_name: str) -> ReadUserPersonalDetails:
        """
        Get user personal details by GitHub username.
        Returns user personal details including:
        - First Name
        - Middle name(s)
        - Last name
        - Bio
        - Location (return null for now)
        - Primary Email
        - Secondary Email
        - University Email
        - Work Email
        - Website/Portfolio Link
        - GitHub Username
        - LinkedIn Username
        - Leetcode Username
        - Dream Company        
        - Dream Company Logo
        - Dream Position
        - Expected Salary Bucket
        - Time Left
        - Tools to Learn
        """
        # Get user by GitHub username
        user = self.get_user_by_github_username(github_user_name)
        
        # Get associated links
        links = None
        try:
            links = self.links_repo.get_by_user_id(user.id)
        except:
            # Links might not exist, continue with None
            pass
        
        # Get location data if user has a location using SQLModel relationship
        location_city = None
        location_state = None
        location_country = None
        location_longitude = None
        location_latitude = None
        
        if user.location_rel:
            location_city = user.location_rel.city
            location_state = user.location_rel.state
            location_country = user.location_rel.country
            location_longitude = user.location_rel.longitude
            location_latitude = user.location_rel.latitude
        
        # Build and return ReadUserPersonalDetails DTO
        return ReadUserPersonalDetails(
            first_name=user.first_name,
            middle_name=user.middle_name,
            last_name=user.last_name,
            bio=user.bio,
            location_city=location_city,
            location_state=location_state,
            location_country=location_country,
            location_longitude=location_longitude,
            location_latitude=location_latitude,
            primary_email=links.primary_email if links else None,
            secondary_email=links.secondary_email if links else None,
            school_email=links.school_email if links else None,
            work_email=links.work_email if links else None,
            portfolio_link=links.portfolio_link if links else None,
            github_user_name=user.github_user_name,
            linkedin_user_name=links.linkedin_user_name if links else None,
            leetcode_user_name=links.leetcode_user_name if links else None,
            dream_company=user.dream_company,
            dream_company_logo=user.dream_company_logo,
            dream_position=user.dream_position,
            expected_salary_bucket=user.expected_salary_bucket,
            time_left=user.time_left,
            tools_to_learn=user.tools_to_learn,
            primary_specialization=user.primary_specialization,
            secondary_specializations=user.secondary_specializations,
            rank=user.rank,
            streak=user.streak,
            onboarding_complete=user.onboarding_complete,
            data_loaded=user.data_loaded,
            onboarding_journey_completed=user.onboarding_journey_completed,
        )

    def get_user_auth_details_by_github_username(self, github_user_name: str) -> ReadUserAuthDetails:
        """
        Get user auth details by GitHub username.
        Returns user auth details including:
        - GitHub username
        - User ID
        - Profile ID
        """
        user = self.get_user_by_github_username(github_user_name)
        profile = self.profile_repo.get_by_user_id(user.id)
        if not profile:
            raise ProfileNotFound(user.id)
        return ReadUserAuthDetails(github_user_name=user.github_user_name, user_id=user.id, profile_id=profile.id)

    def update_user_personal_details_by_github_username(self, github_user_name: str, user_personal_details_update: UpdateUserPersonalDetails) -> ReadUserPersonalDetails:
        """
        Update user personal details by GitHub username.
        Updates both User and Links tables with the provided personal details.
        """
        # Get user by GitHub username
        user = self.get_user_by_github_username(github_user_name)
        
        # Get associated links
        links = None
        try:
            links = self.links_repo.get_by_user_id(user.id)
        except:
            # Links might not exist, we'll create them if needed
            pass
        
        # Update user fields
        update_data = user_personal_details_update.dict(exclude_unset=True)
        
        # Separate user fields, links fields, and location fields
        user_fields = {}
        links_fields = {}
        location_fields = {}
        
        # Fields that belong to User table
        user_table_fields = {
            'first_name', 'middle_name', 'last_name', 'bio',
            'dream_company', 'dream_company_logo', 'dream_position',
            'expected_salary_bucket', 'time_left', 'tools_to_learn',
            'primary_specialization', 'secondary_specializations'
        }
        
        # Fields that belong to Links table
        links_table_fields = {
            'primary_email', 'secondary_email', 'school_email', 'work_email',
            'portfolio_link', 'linkedin_user_name', 'leetcode_user_name'
        }
        
        # Fields that belong to Location table
        location_table_fields = {
            'location_city', 'location_state', 'location_country', 
            'location_longitude', 'location_latitude'
        }
        
        # Separate the fields
        for key, value in update_data.items():
            if key in user_table_fields:
                user_fields[key] = value
            elif key in links_table_fields:
                links_fields[key] = value
            elif key in location_table_fields:
                location_fields[key] = value
        
        # Handle location update if location fields are provided
        if location_fields:
            # Validate that required fields (city and country) are provided
            if 'location_city' not in location_fields or 'location_country' not in location_fields:
                raise ValueError("Both 'location_city' and 'location_country' are required when providing location information")
            
            if user.location:
                # Update existing location
                location_update_data = {
                    'city': location_fields['location_city'],
                    'country': location_fields['location_country'],
                }
                
                # Add optional fields if provided
                if 'location_state' in location_fields:
                    location_update_data['state'] = location_fields['location_state']
                if 'location_longitude' in location_fields:
                    location_update_data['longitude'] = location_fields['location_longitude']
                if 'location_latitude' in location_fields:
                    location_update_data['latitude'] = location_fields['location_latitude']
                
                # Update existing location using LocationService
                location_update = UpdateLocation(**location_update_data)
                self.location_service.update_location(user.location, location_update)
            else:
                # Create new location if user doesn't have one
                from Entities.UserDTOs.location_entity import CreateLocation
                location_create_data = {
                    'city': location_fields['location_city'],
                    'country': location_fields['location_country'],
                }
                
                # Add optional fields if provided
                if 'location_state' in location_fields:
                    location_create_data['state'] = location_fields['location_state']
                if 'location_longitude' in location_fields:
                    location_create_data['longitude'] = location_fields['location_longitude']
                if 'location_latitude' in location_fields:
                    location_create_data['latitude'] = location_fields['location_latitude']
                
                # Create new location using LocationService
                location_create = CreateLocation(**location_create_data)
                created_location = self.location_service.create_location(location_create)
                
                # Set user's location foreign key
                user.location = created_location.id
                user_fields['location'] = created_location.id
        
        # Update user if there are user fields to update
        if user_fields:
            for key, value in user_fields.items():
                setattr(user, key, value)
            self.repo.update(user)
        
        # Update or create links if there are links fields to update
        if links_fields:
            if links:
                # Update existing links
                for key, value in links_fields.items():
                    setattr(links, key, value)
                self.links_repo.update(links)
            else:
                # Create new links record
                links_data = {
                    'user_id': user.id,
                    'github_user_name': user.github_user_name,
                    'github_link': f"https://github.com/{user.github_user_name}",
                }
                links_data.update(links_fields)
                links = Links(**links_data)
                self.links_repo.create(links)
        
        # Return updated personal details
        return self.get_user_personal_details_by_github_username(github_user_name)
        

    def update_user_by_github_username(self, github_username: str, user_update: UpdateUser) -> User:
        """
        Update user by GitHub username.
        Resolves GitHub username to user_id, then calls update_user.
        """
        # Get user by GitHub username to validate it exists and get user_id
        user = self.get_user_by_github_username(github_username)
        return self.update_user(user.id, user_update)

    def delete_user_by_github_username(self, github_username: str) -> str:
        """
        Delete user by GitHub username.
        Resolves GitHub username to user_id, then calls delete_user.
        """
        # Get user by GitHub username to validate it exists and get user_id
        user = self.get_user_by_github_username(github_username)
        return self.delete_user(user.id)