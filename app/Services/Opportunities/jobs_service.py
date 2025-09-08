# services/jobs_service.py
from uuid import UUID
from sqlmodel import Session, select
from typing import List, Optional

from Repository.Opportunities.jobs_repository import JobRepository
from Schema.jobs_schema import CreateJob, UpdateJob
from Entities.SQL.Models.models import Job


class JobService:
    def __init__(self, session: Session):
        self.repo = JobRepository(session)

    def create_job(self, job_create: CreateJob) -> Job:
        job = Job(**job_create.dict(exclude_unset=True))
        return self.repo.create(job)

    def get_job(self, job_id: UUID) -> Optional[Job]:
        return self.repo.get(job_id)

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
            return None
        update_data = job_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(job, key, value)
        return self.repo.update(job)

    def delete_job(self, job_id: UUID) -> Optional[Job]:
        job = self.repo.get(job_id)
        if job:
            self.repo.delete(job)
        return job
