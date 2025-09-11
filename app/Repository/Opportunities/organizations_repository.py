# repositories/organizations_repository.py
from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select

from Schema.SQL.Models.models import Organization

class OrganizationRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, organization: Organization) -> Organization:
        self.session.add(organization)
        self.session.commit()
        self.session.refresh(organization)
        return organization

    def get(self, organization_id: UUID) -> Optional[Organization]:
        statement = select(Organization).where(Organization.id == organization_id)
        return self.session.exec(statement).first()

    def list(self, skip: int = 0, limit: int = 100) -> List[Organization]:
        statement = select(Organization).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def update(self, organization: Organization) -> Organization:
        self.session.add(organization)
        self.session.commit()
        self.session.refresh(organization)
        return organization

    def delete(self, organization: Organization):
        self.session.delete(organization)
        self.session.commit()
