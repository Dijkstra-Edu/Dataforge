from Settings.logging_config import setup_logging
from uuid import UUID
from typing import List, Optional
from sqlmodel import Session
from Repository.User.certifications_repository import CertificationsRepository
from Schema.SQL.Models.models import Certifications
from Utils.Exceptions.user_exceptions import CertificateNotFound , CertificationsUnAvailable
from Entities.UserDTOs.certification_entity import CreateCertification, UpdateCertification


logger = setup_logging()

class CertificateGeneratorService:
        # Placeholder for the actual certificate generation logic
        def __init__(self, session: Session):
            self.repo = CertificationsRepository(session)
        
        def create_certification(self, certification_create: CreateCertification):
            certitification = Certifications(**certification_create.dict(exclude_unset=True))
            return self.repo.create(certitification)
        
        
        def list_all_certifications(self, skip: int =0, limit: int =2, sort_by: str = "created_at",issuing_organization: Optional[str]= None, order: str = "desc", user_id: Optional[UUID] = None ) -> List[Certifications]:
            return self.repo.list( skip=skip, limit=limit, sort_by=sort_by, order=order, user_id=user_id, issuing_organization=issuing_organization)
        
        def get_certification( self, certification_id: UUID) -> Optional[Certifications]:
            certification = self.repo.get(certification_id)
            if not certification:
                raise CertificateNotFound(certification_id)
            return certification
        
        def update_certification( self, certification_id: UUID,  certification_update: UpdateCertification ):
            certification = self.repo.get(certification_id)
            if not certification:
                raise CertificateNotFound(certification_id)
            
            update_data = certification_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(certification, key, value)
            return self.repo.update(certification)
        
        def delete_certification(self, certification_id:UUID) ->Optional[str]:
            certification = self.repo.get(certification_id)
            if not certification:
                raise CertificateNotFound(certification_id)
            self.repo.delete(certification)
            return f"Certification {certification_id} deleted successfully."