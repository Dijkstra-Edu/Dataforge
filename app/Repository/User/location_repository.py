from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from sqlalchemy import asc, desc
from Schema.SQL.Models.models import Location

class LocationRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, location: Location) -> Location:
        self.session.add(location)
        self.session.commit()
        self.session.refresh(location)
        return location

    def get(self, location_id: UUID) -> Optional[Location]:
        statement = select(Location).where(Location.id == location_id)
        return self.session.exec(statement).first()

    def list(
        self,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        order: str = "desc",
        city: Optional[str] = None,
        state: Optional[str] = None,
        country: Optional[str] = None,
    ) -> List[Location]:
        statement = select(Location)

        # Filtering
        if city:
            statement = statement.where(Location.city.ilike(f"%{city}%"))
        if state:
            statement = statement.where(Location.state.ilike(f"%{state}%"))
        if country:
            statement = statement.where(Location.country.ilike(f"%{country}%"))

        # Sorting
        sort_column = getattr(Location, sort_by, Location.created_at)
        if order.lower() == "desc":
            statement = statement.order_by(desc(sort_column))
        else:
            statement = statement.order_by(asc(sort_column))

        # Pagination
        statement = statement.offset(skip).limit(limit)

        return self.session.exec(statement).all()

    def autocomplete(self, query: str, field: str = "city", limit: int = 10) -> List[Location]:
        """
        Autocomplete based on a given field (default: city).
        """
        field_column = getattr(Location, field, Location.city)
        statement = (
            select(Location)
            .where(field_column.ilike(f"%{query}%"))
            .limit(limit)
        )
        return self.session.exec(statement).all()

    def update(self, location: Location) -> Location:
        self.session.add(location)
        self.session.commit()
        self.session.refresh(location)
        return location

    def delete(self, location: Location):
        self.session.delete(location)
        self.session.commit()