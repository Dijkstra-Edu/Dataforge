from uuid import UUID
from typing import List, Optional
from sqlmodel import Session
from Schema.location_schema import CreateLocation, UpdateLocation
from Entities.SQL.Models.models import Location
from Repository.User.location_repository import LocationRepository

class LocationService:
    def __init__(self, session: Session):
        self.repo = LocationRepository(session)

    def create_location(self, location_create: CreateLocation) -> Location:
        location = Location(**location_create.dict(exclude_unset=True))
        return self.repo.create(location)

    def get_location(self, location_id: UUID) -> Optional[Location]:
        return self.repo.get(location_id)

    def list_locations(
        self,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        order: str = "desc",
        city: Optional[str] = None,
        state: Optional[str] = None,
        country: Optional[str] = None,
    ) -> List[Location]:
        """
        Supports pagination, filtering, and sorting.
        """
        return self.repo.list(
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            order=order,
            city=city,
            state=state,
            country=country,
        )

    def autocomplete_locations(
        self,
        query: str,
        field: str = "city",
        limit: int = 10,
    ) -> List[Location]:
        """
        Returns locations where the given field starts with or contains query text.
        """
        return self.repo.autocomplete(query=query, field=field, limit=limit)

    def update_location(self, location_id: UUID, location_update: UpdateLocation) -> Optional[Location]:
        location = self.repo.get(location_id)
        if not location:
            return None
        
        update_data = location_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(location, key, value)
        return self.repo.update(location)

    def delete_location(self, location_id: UUID) -> Optional[Location]:
        location = self.repo.get(location_id)
        if location:
            self.repo.delete(location)
        return location