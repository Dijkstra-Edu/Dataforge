from typing import List, Optional
from uuid import UUID
from sqlmodel import Session

from Entities.SQL.Models.models import Fellowship
from Repository.Opportunities.fellowships_repository import FellowshipRepository
from Schema.fellowships_schema import CreateFellowship, UpdateFellowship


class FellowshipService:
    def __init__(self, session: Session):
        self.repo = FellowshipRepository(session)

    def create_fellowship(self, fellowship_create: CreateFellowship) -> Fellowship:
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
