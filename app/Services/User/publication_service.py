from uuid import UUID
from typing import List, Optional
from sqlmodel import Session

from Schema.SQL.Models.models import Publications, Profile
from Repository.User.publication_repository import PublicationRepository
from Entities.UserDTOs.publication_entity import CreatePublication, UpdatePublication
from Utils.Exceptions.user_exceptions import ProfileNotFound, PublicationNotFound


class PublicationService:
    """
    Service layer for managing Publication entities.
    Handles business logic and delegates DB operations to the repository layer.
    """

    def __init__(self, session: Session):
        self.repo = PublicationRepository(session)
        self.session = session

    def create_publication(self, publication_create: CreatePublication) -> Publications:
        """
        Creates a new publication for a given profile.
        Ensures the associated profile exists before creation.
        """
        profile = self.session.get(Profile, publication_create.profile_id)
        if not profile:
            raise ProfileNotFound(publication_create.profile_id)

        publication = Publications(**publication_create.dict(exclude_unset=True))
        return self.repo.create(publication)

    def get_publication(self, publication_id: UUID) -> Publications:
        """
        Fetch a single publication by its UUID.
        Raises PublicationNotFound if it doesn’t exist.
        """
        publication = self.repo.get(publication_id)
        if not publication:
            raise PublicationNotFound(publication_id)
        return publication

    def list_publications(self, skip: int = 0, limit: int = 20) -> List[Publications]:
        """
        List all publications with pagination.
        Returns an empty list if no publications are found.
        """
        return self.repo.list(skip=skip, limit=limit)

    def get_publications_by_profile_id(self, profile_id: UUID) -> List[Publications]:
        """
        Fetch all publications belonging to a specific profile.
        Returns an empty list if no publications are found.
        """
        return self.repo.get_by_profile_id(profile_id)

    def update_publication(self, publication_id: UUID, publication_update: UpdatePublication) -> Publications:
        """
        Update an existing publication by ID.
        Ensures that if the profile_id is changed, the new profile exists.
        """
        publication = self.repo.get(publication_id)
        if not publication:
            raise PublicationNotFound(publication_id)

        if (
            publication_update.profile_id
            and publication_update.profile_id != publication.profile_id
        ):
            profile = self.session.get(Profile, publication_update.profile_id)
            if not profile:
                raise ProfileNotFound(publication_update.profile_id)

        update_data = publication_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(publication, key, value)

        return self.repo.update(publication)

    def delete_publication(self, publication_id: UUID) -> str:
        """
        Delete a publication by ID.
        Raises PublicationNotFound if the publication doesn’t exist.
        """
        publication = self.repo.get(publication_id)
        if not publication:
            raise PublicationNotFound(publication_id)

        self.repo.delete(publication)
        return f"Publication {publication_id} deleted successfully"
