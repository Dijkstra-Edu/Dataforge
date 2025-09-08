from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from sqlalchemy import asc, desc

from Entities.SQL.Models.models import WorkExperience
from Entities.SQL.Enums.enums import EmploymentType, WorkLocationType, Domain, Tools

class WorkExperienceRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, work_experience: WorkExperience) -> WorkExperience:
        self.session.add(work_experience)
        self.session.commit()
        self.session.refresh(work_experience)
        return work_experience

    def get(self, work_experience_id: UUID) -> Optional[WorkExperience]:
        statement = select(WorkExperience).where(WorkExperience.id == work_experience_id)
        return self.session.exec(statement).first()

    def list(
        self,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        order: str = "desc",
        profile_id: Optional[UUID] = None,
        title: Optional[str] = None,
        company_name: Optional[str] = None,
        employment_type: Optional[EmploymentType] = None,
        domain: Optional[List[Domain]] = None,
        location: Optional[UUID] = None,
        location_type: Optional[WorkLocationType] = None,
        currently_working: Optional[bool] = None,
        start_date_after: Optional[str] = None,
        start_date_before: Optional[str] = None,
    ) -> List[WorkExperience]:
        statement = select(WorkExperience)

        # Filtering
        if profile_id:
            statement = statement.where(WorkExperience.profile_id == profile_id)
        if title:
            statement = statement.where(WorkExperience.title.ilike(f"%{title}%"))
        if company_name:
            statement = statement.where(WorkExperience.company_name.ilike(f"%{company_name}%"))
        if employment_type:
            statement = statement.where(WorkExperience.employment_type == employment_type)
        if domain:
            statement = statement.where(WorkExperience.domain.contains(domain))
        if location:
            statement = statement.where(WorkExperience.location == location)
        if location_type:
            statement = statement.where(WorkExperience.location_type == location_type)
        if currently_working is not None:
            statement = statement.where(WorkExperience.currently_working == currently_working)
        if start_date_after:
            statement = statement.where(WorkExperience.start_date >= start_date_after)
        if start_date_before:
            statement = statement.where(WorkExperience.start_date <= start_date_before)

        # Sorting
        sort_column = getattr(WorkExperience, sort_by, WorkExperience.created_at)
        if order.lower() == "desc":
            statement = statement.order_by(desc(sort_column))
        else:
            statement = statement.order_by(asc(sort_column))

        # Pagination
        statement = statement.offset(skip).limit(limit)

        return self.session.exec(statement).all()

    def get_by_profile_id(self, profile_id: UUID) -> List[WorkExperience]:
        statement = select(WorkExperience).where(WorkExperience.profile_id == profile_id)
        return self.session.exec(statement).all()

    def autocomplete(self, query: str, field: str = "title", limit: int = 10) -> List[WorkExperience]:
        """
        Autocomplete based on a given field (default: title).
        """
        field_column = getattr(WorkExperience, field, WorkExperience.title)
        statement = (
            select(WorkExperience)
            .where(field_column.ilike(f"%{query}%"))
            .limit(limit)
        )
        return self.session.exec(statement).all()

    def update(self, work_experience: WorkExperience) -> WorkExperience:
        self.session.add(work_experience)
        self.session.commit()
        self.session.refresh(work_experience)
        return work_experience

    def delete(self, work_experience: WorkExperience):
        self.session.delete(work_experience)
        self.session.commit()