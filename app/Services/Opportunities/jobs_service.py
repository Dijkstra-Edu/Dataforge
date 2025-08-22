# services/jobs_service.py
from uuid import UUID
from sqlmodel import Session

from Repository.jobs_repository import JobRepository
from Schema.jobs_schema import JobCreate, JobUpdate
from Entities.SQL.Models.models import Job


class JobService:
    def __init__(self, session: Session):
        self.repo = JobRepository(session)

    def create_job(self, job_create: JobCreate) -> Job:
        job = Job(**job_create.dict())
        return self.repo.create(job)

    def get_job(self, job_id: UUID) -> Job:
        return self.repo.get(job_id)

    def list_jobs(self, skip: int = 0, limit: int = 100):
        return self.repo.list(skip, limit)

    def update_job(self, job_id: UUID, job_update: JobUpdate) -> Job:
        job = self.repo.get(job_id)
        if not job:
            return None
        for key, value in job_update.dict(exclude_unset=True).items():
            setattr(job, key, value)
        return self.repo.update(job)

    def delete_job(self, job_id: UUID):
        job = self.repo.get(job_id)
        if job:
            self.repo.delete(job)
        return job
