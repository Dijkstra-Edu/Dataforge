from fastapi import APIRouter, Depends, status
from uuid import UUID
from typing import List
from sqlmodel import Session

from Entities.UserDTOs.document_entity import CreateDocument, UpdateDocument, ReadDocument
from Settings.logging_config import setup_logging
from Services.User.document_service import DocumentService
from db import get_session

logger = setup_logging()

router = APIRouter(prefix="/Dijkstra/v1/document", tags=["Documents"])


@router.post(
    "/create",
    response_model=ReadDocument,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new document",
    description="""
    Create a new document entry for a user's resume/CV.
    
    **Request Body:**
    - `github_username` (string, required): The GitHub username of the user
    - `latex` (string, required): LaTeX preview string of the resume
    - `base_structure` (object, required): JSON structure of the resume data
    
    **Returns:**
    - The created document with its unique `document_id`
    - HTTP 201 Created on success
    - HTTP 404 if the user or profile doesn't exist
    """,
)
async def create_document(
    document_create: CreateDocument,
    session: Session = Depends(get_session),
):
    """Create a new document for a user's resume."""
    service = DocumentService(session)
    document = service.create_document(document_create)
    return ReadDocument.from_orm(document)


@router.get("/{document_id}", response_model=ReadDocument)
def get_document(
    document_id: UUID,
    session: Session = Depends(get_session)
):
    """
    Fetch the latest resume data for a given document_id.
    
    This endpoint:
    - Retrieves a document by its ID
    - Returns both latex and base_structure fields
    - Returns 404 if document not found
    
    **Path Parameters:**
    - document_id: UUID of the document to retrieve
    
    **Returns:**
    - Complete document record with all fields including latex and base_structure
    """
    service = DocumentService(session)
    logger.info(f"Fetching Document with ID: {document_id}")
    document = service.get_document(document_id)
    logger.info(f"Retrieved Document with ID: {document.id}")
    return document


@router.put(
    "/{document_id}",
    response_model=ReadDocument,
    status_code=status.HTTP_200_OK,
    summary="Update an existing document",
    description="""
    Update the LaTeX and/or JSON structure of an existing document.
    
    **Path Parameters:**
    - `document_id` (UUID, required): The ID of the document to update
    
    **Request Body:**
    - `latex` (string, optional): Updated LaTeX preview string
    - `base_structure` (object, optional): Updated JSON structure
    
    You can update one or both fields. Fields not provided will remain unchanged.
    
    **Returns:**
    - The updated document with all fields
    - HTTP 200 OK on success
    - HTTP 404 if the document doesn't exist
    
    **Example:**
    ```json
    {
      "latex": "\\documentclass{article}...",
      "base_structure": {"personal_info": {...}}
    }
    ```
    """,
)
async def update_document(
    document_id: UUID,
    document_update: UpdateDocument,
    session: Session = Depends(get_session),
):
    """Update an existing document's LaTeX and/or base_structure."""
    service = DocumentService(session)
    logger.info(f"Updating Document with ID: {document_id}")
    updated_document = service.update_document(document_id, document_update)
    logger.info(f"Successfully updated Document with ID: {document_id}")
    return ReadDocument.from_orm(updated_document)


@router.get(
    "/user/{github_username}",
    response_model=List[ReadDocument],
    status_code=status.HTTP_200_OK,
    summary="Get all documents for a user",
    description="""
    Retrieve all documents (resumes) for a specific user by their GitHub username.
    
    **Path Parameters:**
    - `github_username` (string, required): The GitHub username of the user
    
    **Returns:**
    - List of all documents for the user (may be empty)
    - HTTP 200 OK on success
    - HTTP 404 if the user or profile doesn't exist
    
    **Use Case:**
    - Fetch all saved resume versions for a user
    - Display resume history
    """,
)
async def get_user_documents(
    github_username: str,
    session: Session = Depends(get_session),
):
    """Get all documents for a user by their GitHub username."""
    service = DocumentService(session)
    logger.info(f"Fetching all documents for user: {github_username}")
    documents = service.get_documents_by_github_username(github_username)
    logger.info(f"Retrieved {len(documents)} document(s) for user: {github_username}")
    return [ReadDocument.from_orm(doc) for doc in documents]


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a document",
    description="""
    Delete a document by its ID.
    
    **Path Parameters:**
    - `document_id` (UUID, required): The ID of the document to delete
    
    **Returns:**
    - Success message
    - HTTP 200 OK on success
    - HTTP 404 if the document doesn't exist
    """,
)
async def delete_document(
    document_id: UUID,
    session: Session = Depends(get_session),
):
    """Delete a document by ID."""
    service = DocumentService(session)
    logger.info(f"Deleting Document with ID: {document_id}")
    message = service.delete_document(document_id)
    logger.info(f"Successfully deleted Document with ID: {document_id}")
    return {"message": message}

