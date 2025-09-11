# services/jobs_service.py
from uuid import UUID
from sqlmodel import Session, select
from typing import List, Optional

from Repository.Opportunities.jobs_repository import JobRepository
from Entities.OpportunityDTOs.jobs_entity import CreateJob, UpdateJob
from Schema.SQL.Models.models import Job, Organization
from Utils.Exceptions.opportunities_exceptions import JobNotFound, OrganizationNotFound
from Utils.Helpers.opportunities_helpers import _validate_tools


class JobService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = JobRepository(session)

    def create_job(self, job_create: CreateJob) -> Job:
        # Check organization exists
        org = self.session.get(Organization, job_create.organization)
        if not org:
            raise OrganizationNotFound(job_create.organization)

        # Validate tools
        _validate_tools(job_create.technologies, "technologies")
        
        job = Job(**job_create.dict(exclude_unset=True))
        return self.repo.create(job)

    def get_job(self, job_id: UUID) -> Optional[Job]:
        job = self.repo.get(job_id)
        if not job:
            raise JobNotFound(job_id)
        return job

    def list_jobs(
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
        """
        Supports pagination, filtering, and sorting.
        """
        return self.repo.list(
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            order=order,
            title=title,
            organization=organization,
            location=location,
            location_type=location_type,
            employment_type=employment_type,
            category=category,
        )

    def autocomplete_jobs(
        self,
        query: str,
        field: str = "title",
        limit: int = 10,
    ) -> List[Job]:
        """
        Returns jobs where the given field starts with or contains query text.
        """
        return self.repo.autocomplete(query=query, field=field, limit=limit)

    def update_job(self, job_id: UUID, job_update: UpdateJob) -> Optional[Job]:
        job = self.repo.get(job_id)
        if not job:
            raise JobNotFound(job_id)
        update_data = job_update.dict(exclude_unset=True)

        # Validate tools if present
        if "technologies" in update_data:
            _validate_tools(update_data["technologies"], "technologies")

        for key, value in update_data.items():
            setattr(job, key, value)
        return self.repo.update(job)

    def delete_job(self, job_id: UUID) -> Optional[str]:
        job = self.repo.get(job_id)
        if not job:
            raise JobNotFound(job_id)
        self.repo.delete(job)
        return f"Job {job_id} deleted successfully"
