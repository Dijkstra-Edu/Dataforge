# controllers/projects_opportunities_controller.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from uuid import UUID
from sqlmodel import Session
from Entities.OpportunityDTOs.projects_opportunities_entity import CreateProject, UpdateProject, ReadProject
from Services.Opportunities.projects_opportunities_service import ProjectsOpportunitiesService
from Settings.logging_config import setup_logging
from db import get_session

logger = setup_logging()

router = APIRouter(prefix="/Dijkstra/v1/projects/opportunities", tags=["ProjectsOpportunities"])

@router.post("/", response_model=ReadProject)
def create_project(project_create: CreateProject, session: Session = Depends(get_session)):
    service = ProjectsOpportunitiesService(session)
    project = service.create_project(project_create)
    logger.info(f"Created project {project.id}")
    return project

@router.get("/{project_id}", response_model=ReadProject)
def get_project(project_id: UUID, session: Session = Depends(get_session)):
    service = ProjectsOpportunitiesService(session)
    project = service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.get("/", response_model=List[ReadProject])
def list_projects(
    skip: int = 0,
    limit: int = 20,
    sort_by: str = Query("created_at"),
    order: str = Query("desc"),
    title: Optional[str] = None,
    organization: Optional[UUID] = None,
    project_level: Optional[str] = None,
    difficulty: Optional[str] = None,
    session: Session = Depends(get_session)
):
    service = ProjectsOpportunitiesService(session)
    filters = {
        "title": title,
        "organization": organization,
        "project_level": project_level,
        "difficulty": difficulty
    }
    return service.list_projects(skip=skip, limit=limit, filters=filters, sort_by=sort_by, order=order)

@router.get("/autocomplete/", response_model=List[ReadProject])
def autocomplete_projects(
    query: str,
    field: str = Query("title"),
    limit: int = 10,
    session: Session = Depends(get_session)
):
    service = ProjectsOpportunitiesService(session)
    return service.autocomplete_projects(query, field, limit)

@router.put("/{project_id}", response_model=ReadProject)
def update_project(project_id: UUID, project_update: UpdateProject, session: Session = Depends(get_session)):
    service = ProjectsOpportunitiesService(session)
    project = service.update_project(project_id, project_update)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.delete("/{project_id}", response_model=ReadProject)
def delete_project(project_id: UUID, session: Session = Depends(get_session)):
    service = ProjectsOpportunitiesService(session)
    project = service.delete_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
