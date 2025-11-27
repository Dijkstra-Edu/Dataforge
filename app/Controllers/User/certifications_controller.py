from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from uuid import UUID

from sqlmodel import Session
from Settings.logging_config import setup_logging
from Services.User.certifications_service import CertificationService
from Entities.UserDTOs.certification_entity import CreateCertification, UpdateCertification, ReadCertification
from db import get_session
logger = setup_logging()

router = APIRouter(prefix="/Dijkstra/v1/certifications", tags=["Certifications"])

@router.post("/", response_model=ReadCertification)
def create_certification( certification_create: CreateCertification, session: Session = Depends(get_session)):
    service  = CertificationService(session)
    logger.info(f"Creating Certificate: {certification_create.name}, {certification_create.credential_id}")
    certificate = service.create_certification(certification_create)
    logger.info(f"Created Certificate with ID: {certificate.id}")
    return certificate

@router.get("/", response_model=List[ReadCertification])
def list_certifications(
    skip: int = 0,
    limit: int = 2,
    sort_by: str = Query("created_at", description="Field to be sorted by"),
    order: str = Query("desc", description="asc or desc"),
    issuing_organization: Optional[str] = None,
    session: Session = Depends(get_session)
):
    service = CertificationService(session)
    logger.info(f"Fetching all certifications: skip={skip}, limit={limit}, sort_by={sort_by}, order={order}, issuing_organization={issuing_organization} ")
    certificates = service.list_all_certifications(skip=skip, limit=limit, sort_by=sort_by,order=order,issuing_organization=issuing_organization)
    return certificates

@router.get("/id/{certification_id}", response_model=ReadCertification)
def get_certification(certification_id: UUID, session: Session = Depends(get_session)):
    service = CertificationService(session)
    logger.info(f"Fetching Certificate with ID: {certification_id}")
    certificate = service.get_certification(certification_id)
    return certificate


@router.get("/{github_username}", response_model=List[ReadCertification])
def get_certifications_by_github_username(github_username: str, session: Session = Depends(get_session)):
    service = CertificationService(session)
    logger.info(f"Fetching Certifications for GitHub username: {github_username}")
    certifications = service.get_certifications_by_github_username(github_username)
    return certifications

@router.put("/{certification_id}", response_model=ReadCertification)
def update_certification(certification_id: UUID,  certification_update: UpdateCertification, session: Session = Depends(get_session)):
    service  = CertificationService(session)
    logger.info(f"Updating Certificate ID: {certification_id} with data {certification_update.dict(exclude_unset=True)}")
    certificate = service.update_certification(certification_id, certification_update)
    logger.info(f"Updated Certificate with ID: {certificate.id}")
    return certificate

@router.delete("/{certification_id}", response_model= ReadCertification )
def delete_certification(certification_id: UUID, session: Session = Depends(get_session)):
    service  = CertificationService(session)
    logger.info(f"Delete Certificate with ID: {certification_id}")
    certification = service.get_certification(certification_id)
    message = service.delete_certification(certification_id)
    logger.info(message)
    return certification


