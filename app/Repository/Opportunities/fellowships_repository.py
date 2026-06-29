from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from sqlalchemy import desc, asc, func
from sqlalchemy.exc import SQLAlchemyError
from Schema.SQL.Models.models import Fellowship, Organization


class FellowshipRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, fellowship: Fellowship) -> Fellowship:
        try:
            self.session.add(fellowship)
            self.session.commit()
            self.session.refresh(fellowship)
            return fellowship
        except SQLAlchemyError as e:
            self.session.rollback()
            raise

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
        organization: Optional[str] = None,
        location: Optional[str] = None,
        featured: Optional[bool] = None,
        location_type: Optional[str] = None,
        duration: Optional[int] = None,
        category: Optional[str] = None,
    ) -> List[Fellowship]:
        statement = select(Fellowship)

        # Filtering
        if title:
            statement = statement.where(Fellowship.title.ilike(f"%{title}%"))
        if organization:
            statement = (
                statement
                .join(Organization, Fellowship.organization == Organization.id)
                .where(Organization.name == organization)
            )
        if location:
            statement = statement.where(Fellowship.location.ilike(f"%{location}%"))
        if featured is not None:
            statement = statement.where(Fellowship.featured == featured)
        if location_type:
             statement = statement.where(Fellowship.location_type == location_type)
        if category:
            statement = statement.where(Fellowship.category == category)
        if duration:
            statement = statement.where(Fellowship.duration_weeks == duration)
        count_statement = select(func.count()).select_from(
            statement.subquery()
        )

        total = self.session.exec(count_statement).one()

        # Sorting
        sort_column = getattr(Fellowship, sort_by, Fellowship.created_at)
        statement = statement.order_by(desc(sort_column) if order.lower() == "desc" else asc(sort_column))

        # Pagination
        statement = statement.offset(skip).limit(limit)

        return self.session.exec(statement).all(), total

    def update(self, fellowship: Fellowship) -> Fellowship:
        self.session.add(fellowship)
        self.session.commit()
        self.session.refresh(fellowship)
        return fellowship

    def delete(self, fellowship: Fellowship):
        try:
            self.session.delete(fellowship)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def autocomplete(self, query: str, field: str = "title", limit: int = 10) -> List[Fellowship]:
        field_column = getattr(Fellowship, field, Fellowship.title)
        statement = select(Fellowship).where(field_column.ilike(f"%{query}%")).limit(limit)
        return self.session.exec(statement).all()
    
     
    def get_distinct_organizations(self) -> List[str]:
        statement = (
            select(Organization.name)
            .join(Fellowship, Fellowship.organization == Organization.id)
            .distinct()
        )
        return [row for row in self.session.exec(statement).all() if row is not None]
    
    def get_distinct_categories(self) -> List[str]:
        statement = select(Fellowship.category).distinct()
        return [row for row in self.session.exec(statement).all() if row is not None]
    
    def get_distinct_durations(self) -> List[str]:
        statement = select(Fellowship.duration_weeks).distinct()
        return [row for row in self.session.exec(statement).all() if row is not None]
    
    def get_distinct_locationTypes(self) -> List[str]:
        statement = select(Fellowship.location_type).distinct()
        return [row for row in self.session.exec(statement).all() if row is not None]