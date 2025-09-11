# repositories/jobs_repository.py
from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from sqlalchemy import asc, desc
from sqlalchemy.exc import SQLAlchemyError

from Entities.SQL.Models.models import Job

class JobRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, job: Job) -> Job:
        try:
            self.session.add(job)
            self.session.commit()
            self.session.refresh(job)
            return job
        except SQLAlchemyError as e:
            self.session.rollback()
            raise

    def get(self, job_id: UUID) -> Optional[Job]:
        statement = select(Job).where(Job.id == job_id)
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
        location_type: Optional[str] = None,
        employment_type: Optional[str] = None,
        category: Optional[str] = None,
    ) -> List[Job]:
        statement = select(Job)

        # Filtering
        if title:
            statement = statement.where(Job.title.ilike(f"%{title}%"))
        if organization:
            statement = statement.where(Job.organization == organization)
        if location:
            statement = statement.where(Job.location.ilike(f"%{location}%"))
        if location_type:
            statement = statement.where(Job.location_type == location_type)
        if employment_type:
            statement = statement.where(Job.employment_type == employment_type)
        if category:
            statement = statement.where(Job.category == category)

        # Sorting
        sort_column = getattr(Job, sort_by, Job.created_at)
        if order.lower() == "desc":
            statement = statement.order_by(desc(sort_column))
        else:
            statement = statement.order_by(asc(sort_column))

        # Pagination
        statement = statement.offset(skip).limit(limit)

        return self.session.exec(statement).all()

    def autocomplete(self, query: str, field: str = "title", limit: int = 10) -> List[Job]:
        """
        Autocomplete based on a given field (default: title).
        """
        field_column = getattr(Job, field, Job.title)
        statement = (
            select(Job)
            .where(field_column.ilike(f"%{query}%"))
            .limit(limit)
        )
        return self.session.exec(statement).all()

    def update(self, job: Job) -> Job:
        try:
            self.session.add(job)
            self.session.commit()
            self.session.refresh(job)
            return job
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def delete(self, job: Job):
        try:
            self.session.delete(job)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise
