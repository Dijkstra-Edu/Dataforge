# services/organization_service.py
from uuid import UUID
from sqlmodel import Session

from Repository.Opportunities.organizations_repository import OrganizationRepository
from Entities.OpportunityDTOs.organization_entity import CreateOrganization, UpdateOrganization
from Schema.SQL.Models.models import Organization
from Utils.Exceptions.opportunities_exceptions import OrganizationNotFound

class OrganizationService:
    def __init__(self, session: Session):
        self.repo = OrganizationRepository(session)

    def create_organization(self, org_create: CreateOrganization) -> Organization:
        org = Organization(**org_create.dict(exclude_unset=True))
        return self.repo.create(org)

    def get_organization(self, org_id: UUID) -> Organization:
        org = self.repo.get(org_id)
        if not org:
            raise OrganizationNotFound(org_id)
        return org

    def list_organizations(self, skip: int = 0, limit: int = 100):
        return self.repo.list(skip, limit)

    def update_organization(self, org_id: UUID, org_update: UpdateOrganization) -> Organization:
        org = self.repo.get(org_id)
        if not org:
            raise OrganizationNotFound(org_id)
        update_data = org_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(org, key, value)
        return self.repo.update(org)

    def delete_organization(self, org_id: UUID):
        org = self.repo.get(org_id)
        if not org:
            raise OrganizationNotFound(org_id)
        self.repo.delete(org)
        return org
