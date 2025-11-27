from Settings.logging_config import setup_logging
from uuid import UUID
from typing import List, Optional
from sqlmodel import Session
from Repository.User.certifications_repository import CertificationsRepository
from Schema.SQL.Models.models import Certifications
from Utils.Exceptions.user_exceptions import CertificationNotFound
from Entities.UserDTOs.certification_entity import CreateCertification, UpdateCertification


logger = setup_logging()

class CertificationService:
       
        def __init__(self, session: Session):
            self.repo = CertificationsRepository(session)
            self.session = session
        
        def create_certification(self, certification_create: CreateCertification):
            certitification = Certifications(**certification_create.dict(exclude_unset=True))
            return self.repo.create(certitification)
        
        
        def list_all_certifications(self, skip: int =0, limit: int =2, sort_by: str = "created_at",issuing_organization: Optional[str]= None, order: str = "desc", user_id: Optional[UUID] = None ) -> List[Certifications]:
            certifications =  self.repo.list( skip=skip, limit=limit, sort_by=sort_by, order=order, user_id=user_id, issuing_organization=issuing_organization)
            if not certifications:
                raise CertificationNotFound()
            return certifications
        
        def get_certification( self, certification_id: UUID) -> Optional[Certifications]:
            certification = self.repo.get(certification_id)
            if not certification:
                raise CertificationNotFound(certification_id)
            return certification
        
        def update_certification( self, certification_id: UUID,  certification_update: UpdateCertification ):
            certification = self.repo.get(certification_id)
            if not certification:
                raise CertificationNotFound(certification_id)
            
            update_data = certification_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(certification, key, value)
            return self.repo.update(certification)
        
        def delete_certification(self, certification_id:UUID) ->Optional[str]:
            certification = self.repo.get(certification_id)
            if not certification:
                raise CertificationNotFound(certification_id)
            self.repo.delete(certification)
            return f"Certification {certification_id} deleted successfully."
        
        def get_certifications_by_profile(self, profile_id: UUID) -> List[Certifications]:
            """
            Get all certifications for a specific profile.
            Returns empty list if no certifications found.
            """
            certifications = self.repo.get_by_profile_id(profile_id)
            return certifications if certifications else []
        
        def get_certifications_by_github_username(self, github_username: str) -> List[Certifications]:
            """Get all certifications by GitHub username"""
            from Services.User.profile_service import ProfileService
            
            profile_service = ProfileService(self.session)
            profile_id = profile_service.get_profile_id_by_github_username(github_username)
            return self.get_certifications_by_profile(profile_id)