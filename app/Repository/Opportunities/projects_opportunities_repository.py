# repositories/projects_opportunities_repository.py
from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from Entities.SQL.Models.models import ProjectsOpportunities

class ProjectsOpportunitiesRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, project: ProjectsOpportunities) -> ProjectsOpportunities:
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)
        return project

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
    ) -> List[ProjectsOpportunities]:
        statement = select(ProjectsOpportunities)
        
        for field, value in filters.items():
            if value is not None:
                column = getattr(ProjectsOpportunities, field, None)
                if column is not None:
                    statement = statement.where(column == value)
        
        if order.lower() == "desc":
            statement = statement.order_by(getattr(ProjectsOpportunities, sort_by).desc())
        else:
            statement = statement.order_by(getattr(ProjectsOpportunities, sort_by).asc())
        
        statement = statement.offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def autocomplete(self, query: str, field: str = "title", limit: int = 10):
        column = getattr(ProjectsOpportunities, field, None)
        if column is None:
            column = ProjectsOpportunities.title
        statement = select(ProjectsOpportunities).where(column.ilike(f"%{query}%")).limit(limit)
        return self.session.exec(statement).all()

    def update(self, project: ProjectsOpportunities) -> ProjectsOpportunities:
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)
        return project

    def delete(self, project: ProjectsOpportunities):
        self.session.delete(project)
        self.session.commit()
