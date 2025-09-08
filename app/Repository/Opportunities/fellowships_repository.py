from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from sqlalchemy import desc, asc

from Entities.SQL.Models.models import Fellowship


class FellowshipRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, fellowship: Fellowship) -> Fellowship:
        self.session.add(fellowship)
        self.session.commit()
        self.session.refresh(fellowship)
        return fellowship

    def get(self, fellowship_id: UUID) -> Optional[Fellowship]:
        statement = select(Fellowship).where(Fellowship.id == fellowship_id)
        return self.session.exec(statement).first()

    def list(
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
        statement = select(Fellowship)

        # Filtering
        if title:
            statement = statement.where(Fellowship.title.ilike(f"%{title}%"))
        if organization:
            statement = statement.where(Fellowship.organization == organization)
        if location:
            statement = statement.where(Fellowship.location.ilike(f"%{location}%"))
        if featured is not None:
            statement = statement.where(Fellowship.featured == featured)

        # Sorting
        sort_column = getattr(Fellowship, sort_by, Fellowship.created_at)
        statement = statement.order_by(desc(sort_column) if order.lower() == "desc" else asc(sort_column))

        # Pagination
        statement = statement.offset(skip).limit(limit)

        return self.session.exec(statement).all()

    def update(self, fellowship: Fellowship) -> Fellowship:
        self.session.add(fellowship)
        self.session.commit()
        self.session.refresh(fellowship)
        return fellowship

    def delete(self, fellowship: Fellowship):
        self.session.delete(fellowship)
        self.session.commit()

    def autocomplete(self, query: str, field: str = "title", limit: int = 10) -> List[Fellowship]:
        field_column = getattr(Fellowship, field, Fellowship.title)
        statement = select(Fellowship).where(field_column.ilike(f"%{query}%")).limit(limit)
        return self.session.exec(statement).all()
