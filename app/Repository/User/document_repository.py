from typing import Optional
from uuid import UUID
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError
from Schema.SQL.Models.models import Document


class DocumentRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, document: Document) -> Document:
        """Create a new document record."""
        try:
            self.session.add(document)
            self.session.commit()
            self.session.refresh(document)
            return document
        except SQLAlchemyError as e:
            self.session.rollback()
            raise
    
    def get(self, document_id: UUID) -> Optional[Document]:
        """Get a document by its ID."""
        statement = select(Document).where(Document.id == document_id)
        return self.session.exec(statement).first()
    
    def update(self, document: Document) -> Document:
        """Update an existing document."""
        try:
            self.session.add(document)
            self.session.commit()
            self.session.refresh(document)
            return document
        except SQLAlchemyError:
            self.session.rollback()
            raise
    
    def delete(self, document: Document):
        """Delete a document."""
        try:
            self.session.delete(document)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise
    
    def get_by_profile_id(self, profile_id: UUID) -> list[Document]:
        """Get all documents for a specific profile."""
        statement = select(Document).where(Document.profile_id == profile_id)
        return self.session.exec(statement).all()
