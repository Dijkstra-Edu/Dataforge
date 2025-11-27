from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from sqlalchemy import asc, desc
from sqlalchemy.exc import SQLAlchemyError
from Schema.SQL.Models.models import Certifications, Profile, User

class CertificationsRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def create( self, certifications: Certifications) -> Certifications:
        try:
            self.session.add(certifications)
            self.session.commit()
            self.session.refresh(certifications)
            return certifications
        except SQLAlchemyError as e:
            self.session.rollback()
            raise
        
    def list(
        self,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        order: str = "desc",
        issuing_organization: Optional[str] = None,
        user_id: Optional[UUID] = None,
    ) -> List[Certifications]:
        """List certifications with optional filtering and sorting.

        Args:
            skip: Number of records to skip (pagination offset)
            limit: Max records to return
            sort_by: Column name on Certifications to sort by
            order: asc or desc
            issuing_organization: Case-insensitive partial match on issuing organization
            user_id: (Optional) Filter certifications that belong to a given User (via Profile relation)
        """
        statement = select(Certifications)

        if user_id:
            statement = (
                statement.join(Profile, Profile.id == Certifications.profile_id)
                .join(User, User.id == Profile.user_id)
                .where(User.id == user_id)
            )

        
        if issuing_organization:
            issuing_organization = issuing_organization.strip()
            if issuing_organization:
                statement = statement.where(
                    Certifications.issuing_organization.ilike(f"%{issuing_organization}%")
                )

        # Sorting (fallback to created_at if invalid)
        sort_column = getattr(Certifications, sort_by, Certifications.created_at)
        if order.lower() == "desc":
            statement = statement.order_by(desc(sort_column))
        else:
            statement = statement.order_by(asc(sort_column))

        # Pagination
        statement = statement.offset(skip).limit(limit)

        return self.session.exec(statement).all()
        
    def get( self, certification_id: UUID) -> Optional[Certifications]:
        statement = select(Certifications).where(Certifications.id == certification_id )
        return self.session.exec(statement).first()
    
    
    def update( self, certification: Certifications) -> Certifications:
        try:
            self.session.add(certification)
            self.session.commit()
            self.session.refresh(certification)
            return certification
        except SQLAlchemyError:
            self.session.rollback()
            raise
    
    def delete(self, certification: Certifications):
        try:
            self.session.delete( certification)
            self.session.commit()
        except SQLAlchemyError:
            raise
    
    def get_by_profile_id(self, profile_id: UUID) -> List[Certifications]:
        """Get all certifications for a specific profile."""
        statement = select(Certifications).where(Certifications.profile_id == profile_id)
        return self.session.exec(statement).all()
    