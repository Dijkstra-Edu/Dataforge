from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlmodel import Session

from Entities.SQL.Models.models import Fellowship, Organization
from Repository.Opportunities.fellowships_repository import FellowshipRepository
from Schema.fellowships_schema import CreateFellowship, UpdateFellowship
from Entities.SQL.Enums.enums import Tools


class FellowshipService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = FellowshipRepository(session)

    def create_fellowship(self, fellowship_create: CreateFellowship) -> Fellowship:
        # Check if the organization exists
        org = self.session.get(Organization, fellowship_create.organization)
        if not org:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Organization with ID {fellowship_create.organization} does not exist."
            )
        
        # Validate technologies
        if fellowship_create.technologies:
            invalid_techs = [
                tech for tech in fellowship_create.technologies
                if tech not in Tools._value2member_map_
            ]
            if invalid_techs:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid technologies: {invalid_techs}. Must be one of {list(Tools)}"
                )
        
        fellowship = Fellowship(**fellowship_create.dict(exclude_unset=True))
        return self.repo.create(fellowship)

    def get_fellowship(self, fellowship_id: UUID) -> Optional[Fellowship]:
        return self.repo.get(fellowship_id)

    def list_fellowships(
        self,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        order: str = "desc",
        title: Optional[str] = None,
        organization: Optional[UUID] = None,
        location: Optional[str] = None,
        featured: Optional[bool] = None,
    ) -> List[Fellowship]:
        return self.repo.list(skip, limit, sort_by, order, title, organization, location, featured)

    def update_fellowship(self, fellowship_id: UUID, fellowship_update: UpdateFellowship) -> Optional[Fellowship]:
        fellowship = self.repo.get(fellowship_id)
        if not fellowship:
            return None
        update_data = fellowship_update.dict(exclude_unset=True)

        # Validate technologies if present
        if "technologies" in update_data:
            invalid_techs = [
                tech for tech in update_data["technologies"]
                if tech not in Tools._value2member_map_
            ]
            if invalid_techs:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid technologies: {invalid_techs}. Must be one of {list(Tools)}"
                )
        
        for key, value in update_data.items():
            setattr(fellowship, key, value)
        return self.repo.update(fellowship)

    def delete_fellowship(self, fellowship_id: UUID) -> Optional[Fellowship]:
        fellowship = self.repo.get(fellowship_id)
        if fellowship:
            self.repo.delete(fellowship)
        return fellowship

    def autocomplete_fellowships(self, query: str, field: str = "title", limit: int = 10) -> List[Fellowship]:
        return self.repo.autocomplete(query, field, limit)
