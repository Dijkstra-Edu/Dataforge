# repositories/projects_opportunities_repository.py
from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, func, select
from Schema.SQL.Models.models import Job, Job, ProjectsOpportunities
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import ARRAY
class ProjectsOpportunitiesRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, project: ProjectsOpportunities) -> ProjectsOpportunities:
        try:
            self.session.add(project)
            self.session.commit()
            self.session.refresh(project)
            return project
        except SQLAlchemyError as e:
            self.session.rollback()
            raise

    def get(self, project_id: UUID) -> Optional[ProjectsOpportunities]:
        statement = select(ProjectsOpportunities).where(ProjectsOpportunities.id == project_id)
        return self.session.exec(statement).first()

    def list(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: dict = {},
        sort_by: str = "created_at",
        order: str = "desc"
    ):
        statement = select(ProjectsOpportunities)
        for field, value in filters.items():
            if value is not None:
                if field == "title":
                    statement = statement.where(ProjectsOpportunities.title.ilike(f"%{value}%"))
                    continue
                column = getattr(ProjectsOpportunities, field, None)
                if column is not None:
                    if isinstance(column.type, ARRAY):
                        statement = statement.where(column.any(value))
                    else:
                        statement = statement.where(column == value)
         # Count query BEFORE pagination
        count_statement = select(func.count()).select_from(
            statement.subquery()
        )
        total = self.session.exec(count_statement).one()
        if order.lower() == "desc":
            statement = statement.order_by(getattr(ProjectsOpportunities, sort_by).desc())
        else:
            statement = statement.order_by(getattr(ProjectsOpportunities, sort_by).asc())
        
        statement = statement.offset(skip).limit(limit)
        return self.session.exec(statement).all(), total

    def autocomplete(self, query: str, field: str = "title", limit: int = 10):
        column = getattr(ProjectsOpportunities, field, None)
        if column is None:
            column = ProjectsOpportunities.title
        statement = select(ProjectsOpportunities).where(column.ilike(f"%{query}%")).limit(limit)
        return self.session.exec(statement).all()

    def update(self, project: ProjectsOpportunities) -> ProjectsOpportunities:
        try:
            self.session.add(project)
            self.session.commit()
            self.session.refresh(project)
            return project
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def delete(self, project: ProjectsOpportunities):
        try:
            self.session.delete(project)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def get_distinct_languages(self) -> List[str]:
        statement = select(ProjectsOpportunities.languages).distinct()
        return [row for row in self.session.exec(statement).all() if row is not None]
    
    def get_distinct_frameworks(self) -> List[str]:
        statement = select(ProjectsOpportunities.frameworks).distinct()
        return [row for row in self.session.exec(statement).all() if row is not None]
    
    def get_distinct_organizations(self) -> List[str]:
        statement = select(ProjectsOpportunities.organization).distinct()
        return [row for row in self.session.exec(statement).all() if row is not None]

    def get_distinct_categories(self) -> List[str]:
        statement = select(ProjectsOpportunities.category)
        result = list({
            item
            for row in self.session.exec(statement).all()
            if row is not None
            for item in row
        })
        return result    
    def get_distinct_difficulties(self) -> List[str]:
        statement = select(ProjectsOpportunities.difficulty).distinct()
        return [row for row in self.session.exec(statement).all() if row is not None]
    
    def get_distinct_licenses(self) -> List[str]:
        statement = select(ProjectsOpportunities.license).distinct()
        return [row for row in self.session.exec(statement).all() if row is not None]