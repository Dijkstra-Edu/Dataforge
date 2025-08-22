# repositories/jobs_repository.py
from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select

from Entities.SQL.Models.models import Job

class JobRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, job: Job) -> Job:
        self.session.add(job)
        self.session.commit()
        self.session.refresh(job)
        return job

    def get(self, job_id: UUID) -> Optional[Job]:
        statement = select(Job).where(Job.id == job_id)
        return self.session.exec(statement).first()

    def list(self, skip: int = 0, limit: int = 100) -> List[Job]:
        statement = select(Job).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def update(self, job: Job) -> Job:
        self.session.add(job)
        self.session.commit()
        self.session.refresh(job)
        return job

    def delete(self, job: Job):
        self.session.delete(job)
        self.session.commit()
