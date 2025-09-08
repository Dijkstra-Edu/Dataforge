# controllers/organizations_controller.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from uuid import UUID
from sqlmodel import Session
from Schema.organization_schema import CreateOrganization, UpdateOrganization
from Services.Opportunities.organization_service import OrganizationService
from Settings.logging_config import setup_logging
from Schema.organization_schema import ReadOrganization
from db import get_session

logger = setup_logging()

router = APIRouter(prefix="/Dijkstra/v1/organizations", tags=["Organizations"])

@router.post("/", response_model=ReadOrganization)
def create_organization(org_create: CreateOrganization, session: Session = Depends(get_session)):
    service = OrganizationService(session)
    logger.info(f"Creating organization: {org_create.name}")
    org = service.create_organization(org_create)
    logger.info(f"Created organization with ID: {org.id}")
    return org

@router.get("/{org_id}", response_model=ReadOrganization)
def get_organization(org_id: UUID, session: Session = Depends(get_session)):
    service = OrganizationService(session)
    logger.info(f"Fetching organization with ID: {org_id}")
    org = service.get_organization(org_id)
    if not org:
        logger.warning(f"Organization not found: {org_id}")
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

@router.get("/", response_model=List[ReadOrganization])
def list_organizations(
    skip: int = 0,
    limit: int = 20,
    session: Session = Depends(get_session),
):
    service = OrganizationService(session)
    logger.info(f"Listing organizations: skip={skip}, limit={limit}")
    orgs = service.list_organizations(skip=skip, limit=limit)
    logger.info(f"Returned {len(orgs)} organizations")
    return orgs

@router.put("/{org_id}", response_model=ReadOrganization)
def update_organization(org_id: UUID, org_update: UpdateOrganization, session: Session = Depends(get_session)):
    service = OrganizationService(session)
    logger.info(f"Updating organization ID: {org_id} with data: {org_update.dict(exclude_unset=True)}")
    org = service.update_organization(org_id, org_update)
    if not org:
        logger.warning(f"Attempted update for missing organization: {org_id}")
        raise HTTPException(status_code=404, detail="Organization not found")
    logger.info(f"Updated organization ID: {org.id}")
    return org

@router.delete("/{org_id}", response_model=ReadOrganization)
def delete_organization(org_id: UUID, session: Session = Depends(get_session)):
    service = OrganizationService(session)
    logger.info(f"Deleting organization ID: {org_id}")
    org = service.delete_organization(org_id)
    if not org:
        logger.warning(f"Attempted delete for missing organization: {org_id}")
        raise HTTPException(status_code=404, detail="Organization not found")
    logger.info(f"Deleted organization ID: {org.id}")
    return org
