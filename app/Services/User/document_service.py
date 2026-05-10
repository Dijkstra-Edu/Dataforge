from Settings.logging_config import get_logger
from uuid import UUID
from typing import Optional
from sqlmodel import Session
from Repository.User.document_repository import DocumentRepository
from Repository.User.profile_repository import ProfileRepository
from Schema.SQL.Models.models import Document
from Entities.UserDTOs.document_entity import CreateDocument, UpdateDocument
from Utils.Exceptions.user_exceptions import DocumentNotFound, ProfileNotFound

logger = get_logger()

class DocumentService:
    
    def __init__(self, session: Session):
        self.repo = DocumentRepository(session)
        self.profile_repo = ProfileRepository(session)
        self.session = session
    
    def create_document(self, document_create: CreateDocument) -> Document:
        """Create a new document using profile username to find the profile."""
        profile = self.profile_repo.get_by_username(document_create.username)
        if not profile:
            raise ProfileNotFound(f"Profile not found for username '{document_create.username}'")
        
        # Create document with the found profile_id
        document = Document(
            profile_id=profile.id,
            document_name=document_create.document_name,
            document_type=document_create.document_type,
            document_kind=document_create.document_kind,
            latex=document_create.latex,
            base_structure=document_create.base_structure
        )
        return self.repo.create(document)
    
    def get_document(self, document_id: UUID) -> Optional[Document]:
        """Get a document by ID."""
        document = self.repo.get(document_id)
        if not document:
            raise DocumentNotFound(document_id)
        return document
    
    def update_document(self, document_id: UUID, document_update: UpdateDocument) -> Document:
        """Update an existing document."""
        document = self.repo.get(document_id)
        if not document:
            raise DocumentNotFound(document_id)
        
        update_data = document_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(document, key, value)
        
        return self.repo.update(document)
    
    def delete_document(self, document_id: UUID) -> str:
        """Delete a document by ID."""
        document = self.repo.get(document_id)
        if not document:
            raise DocumentNotFound(document_id)
        
        self.repo.delete(document)
        return f"Document {document_id} deleted successfully."
    
    def get_documents_by_profile(self, profile_id: UUID) -> list[Document]:
        """Get all documents for a specific profile."""
        documents = self.repo.get_by_profile_id(profile_id)
        return documents if documents else []
    
    def get_documents_by_github_username(self, github_username: str) -> list[Document]:
        """Get all documents for a user by GitHub username."""
        profile = self.profile_repo.get_by_username(github_username)

        if not profile:
            raise ProfileNotFound(f"Profile not found for username '{github_username}'")
        
        # Get all documents for this profile
        documents = self.repo.get_by_profile_id(profile.id)
        return documents if documents else []
