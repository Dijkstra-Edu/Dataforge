from uuid import UUID
from typing import List, Optional
from sqlmodel import Session

from Schema.SQL.Models.models import User, Links
from Repository.User.links_repository import LinksRepository
from Entities.UserDTOs.links_entity import CreateLinks, UpdateLinks
from Utils.Exceptions.user_exceptions import (
    UserNotFound,
    LinksNotFound,
    LinksAlreadyExists,
)


class LinksService:
    def __init__(self, session: Session):
        self.repo = LinksRepository(session)
        self.session = session

    def create_links(self, links_create: CreateLinks) -> Links:
        user = self.session.get(User, links_create.user_id)
        if not user:
            raise UserNotFound(links_create.user_id)

        existing = self.repo.get_by_user_id(links_create.user_id)
        if existing:
            raise LinksAlreadyExists(links_create.user_id)

        links = Links(**links_create.dict(exclude_unset=True))
        return self.repo.create(links)

    def get_links(self, link_id: UUID) -> Links:
        links = self.repo.get(link_id)
        if not links:
            raise LinksNotFound(link_id)
        return links

    def get_links_by_user_id(self, user_id: UUID) -> Links:
        links = self.repo.get_by_user_id(user_id)
        if not links:
            raise LinksNotFound(user_id)
        return links

    def get_links_by_github_username(self, github_username: str) -> Links:
        """Get links by GitHub username"""
        from Services.User.user_service import UserService
        
        user_service = UserService(self.session)
        user_id = user_service.get_user_id_by_github_username(github_username)
        return self.get_links_by_user_id(user_id)

    def list_links(
        self,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        order: str = "desc",
        github_user_name: Optional[str] = None,
        linkedin_user_name: Optional[str] = None,
        leetcode_user_name: Optional[str] = None,
        orcid_id: Optional[str] = None,
        primary_email: Optional[str] = None,
        secondary_email: Optional[str] = None,
        school_email: Optional[str] = None,
        work_email: Optional[str] = None,
    ) -> List[Links]:
        """
        Supports pagination, filtering, and sorting.
        """
        return self.repo.list(
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            order=order,
            github_user_name=github_user_name,
            linkedin_user_name=linkedin_user_name,
            leetcode_user_name=leetcode_user_name,
            orcid_id=orcid_id,
            primary_email=primary_email,
            secondary_email=secondary_email,
            school_email=school_email,
            work_email=work_email,
        )

    def update_links(self, link_id: UUID, links_update: UpdateLinks) -> Links:
        links = self.repo.get(link_id)
        if not links:
            raise LinksNotFound(link_id)

        update_data = links_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(links, key, value)

        return self.repo.update(links)

    
    def delete_links(self, link_id: UUID) -> str:
        links = self.repo.get(link_id)
        if not links:
            raise LinksNotFound(link_id)

        self.repo.delete(links)
        return f"Links {link_id} deleted successfully"

    def update_links_by_github_username(self, github_username: str, links_update: UpdateLinks) -> Links:
        """
        Update links by GitHub username.
        Resolves GitHub username to user_id, then to links_id, then updates.
        """
        from Services.User.user_service import UserService
        
        # Get user by GitHub username to validate it exists and get user_id
        user_service = UserService(self.session)
        user_id = user_service.get_user_id_by_github_username(github_username)
        
        # Get links by user_id to get link_id
        links = self.get_links_by_user_id(user_id)
        
        # Update the links using the existing method
        return self.update_links(links.id, links_update)

    def delete_links_by_github_username(self, github_username: str) -> str:
        """
        Delete links by GitHub username.
        Resolves GitHub username to user_id, then to links_id, then deletes.
        """
        from Services.User.user_service import UserService
        
        # Get user by GitHub username to validate it exists and get user_id
        user_service = UserService(self.session)
        user_id = user_service.get_user_id_by_github_username(github_username)
        
        # Get links by user_id to get link_id
        links = self.get_links_by_user_id(user_id)
        
        # Delete the links using the existing method
        return self.delete_links(links.id)