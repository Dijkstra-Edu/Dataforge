from typing import List, Optional
from uuid import UUID
from sqlmodel import Session

from Schema.SQL.Models.models import Fellowship, Organization
from Repository.Opportunities.fellowships_repository import FellowshipRepository
from Entities.OpportunityDTOs.fellowships_entity import CreateFellowship, PaginatedReadFellowships, ReadFellowship, UpdateFellowship
from Schema.SQL.Enums.enums import Tools
from Utils.Exceptions.opportunities_exceptions import FellowshipNotFound, OrganizationNotFound
from Utils.Helpers.opportunities_helpers import _validate_tools


class FellowshipService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = FellowshipRepository(session)

    def create_fellowship(self, fellowship_create: CreateFellowship) -> Fellowship:
        # Check organization exists
        org = self.session.get(Organization, fellowship_create.organization)
        if not org:
            raise OrganizationNotFound(fellowship_create.organization)

        # Validate tools
        _validate_tools(fellowship_create.technologies, "technologies")
        
        fellowship = Fellowship(**fellowship_create.dict(exclude_unset=True))
        return self.repo.create(fellowship)

    def get_fellowship(self, fellowship_id: UUID) -> Optional[Fellowship]:
        fellowship = self.repo.get(fellowship_id)
        if not fellowship:
            raise FellowshipNotFound(fellowship_id)
        return fellowship

    def list_fellowships(
        self,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        order: str = "desc",
        title: Optional[str] = None,
        organization: Optional[str] = None,
        location: Optional[str] = None,
        featured: Optional[bool] = None,
        location_type: Optional[str] = None,
        duration: Optional[int] = None,
        category: Optional[str] = None,
    ) -> PaginatedReadFellowships:
        fellowship_db_models, total = self.repo.list(
            skip,
            limit,
            sort_by,
            order,
            title,
            organization,
            location,
            featured,
            location_type,
            duration,
            category,
        )

        response_list = []

        for fellowship in fellowship_db_models:
            dto = ReadFellowship.model_validate(fellowship, from_attributes=True)
            dto.organization_logo = fellowship.organization_rel.image
            response_list.append(dto)

        return PaginatedReadFellowships(
            fellowships=response_list,
            total=total
        )
                

    def update_fellowship(self, fellowship_id: UUID, fellowship_update: UpdateFellowship) -> Optional[Fellowship]:
        fellowship = self.repo.get(fellowship_id)
        if not fellowship:
            raise FellowshipNotFound(fellowship_id)
        update_data = fellowship_update.dict(exclude_unset=True)

        # Validate tools if present
        if "technologies" in update_data:
            _validate_tools(update_data["technologies"], "technologies")
        
        for key, value in update_data.items():
            setattr(fellowship, key, value)
        return self.repo.update(fellowship)

    def delete_fellowship(self, fellowship_id: UUID) -> Optional[str]:
        fellowship = self.repo.get(fellowship_id)
        if not fellowship:
            raise FellowshipNotFound(fellowship_id)
        self.repo.delete(fellowship)
        return f"Fellowship {fellowship_id} deleted successfully"

    def autocomplete_fellowships(self, query: str, field: str = "title", limit: int = 10) -> List[Fellowship]:
        return self.repo.autocomplete(query, field, limit)

    def get_filter_helpers(self) -> dict:
        return {
            "locationTypes": self.repo.get_distinct_locationTypes(),
            "categories": self.repo.get_distinct_categories(),
            "durations": self.repo.get_distinct_durations(),
            "organizations": self.repo.get_distinct_organizations()
        }