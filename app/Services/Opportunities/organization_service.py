# services/organization_service.py
from uuid import UUID
from sqlmodel import Session

from Repository.Opportunities.organizations_repository import OrganizationRepository
from Schema.organization_schema import CreateOrganization, UpdateOrganization
from Entities.SQL.Models.models import Organization

class OrganizationService:
    def __init__(self, session: Session):
        self.repo = OrganizationRepository(session)

    def create_organization(self, org_create: CreateOrganization) -> Organization:
        org = Organization(**org_create.dict(exclude_unset=True))
        return self.repo.create(org)

    def get_organization(self, org_id: UUID) -> Organization:
        return self.repo.get(org_id)

    def list_organizations(self, skip: int = 0, limit: int = 100):
        return self.repo.list(skip, limit)

    def update_organization(self, org_id: UUID, org_update: UpdateOrganization) -> Organization:
        org = self.repo.get(org_id)
        if not org:
            return None
        update_data = org_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(org, key, value)
        return self.repo.update(org)

    def delete_organization(self, org_id: UUID):
        org = self.repo.get(org_id)
        if org:
            self.repo.delete(org)
        return org
