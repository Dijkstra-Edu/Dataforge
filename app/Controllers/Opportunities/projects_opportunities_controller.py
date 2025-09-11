# controllers/projects_opportunities_controller.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from uuid import UUID
from sqlmodel import Session
from Schema.projects_opportunities_schema import CreateProject, UpdateProject, ReadProject
from Services.Opportunities.projects_opportunities_service import ProjectsOpportunitiesService
from Settings.logging_config import setup_logging
from Utils.errors import raise_api_error
from Utils.error_codes import ErrorCodes
from db import get_session

logger = setup_logging()

router = APIRouter(prefix="/Dijkstra/v1/projects/opportunities", tags=["ProjectsOpportunities"])

@router.post("/", response_model=ReadProject)
def create_project(project_create: CreateProject, session: Session = Depends(get_session)):
    try:
        service = ProjectsOpportunitiesService(session)
        project = service.create_project(project_create)
        logger.info(f"Created project {project.id}")
        return project
    except Exception as e:
        logger.error(f"Error creating project: {str(e)}")
        raise_api_error(
            code=ErrorCodes.OPPT_PROJ_DB_A01,
            error="Failed to create project",
            detail=str(e.orig) if e.args else "An unexpected error occurred.",
            status=500
        )

@router.get("/{project_id}", response_model=ReadProject)
def get_project(project_id: UUID, session: Session = Depends(get_session)):
    try:
        service = ProjectsOpportunitiesService(session)
        project = service.get_project(project_id)
        if not project:
            logger.warning(f"Project {project_id} not found")
            raise HTTPException(status_code=404, detail="Project not found")
        return project
    except Exception as e:
        logger.error(f"Error fetching project {project_id}: {str(e)}")
        raise_api_error(
            code=ErrorCodes.OPPT_PROJ_DB_A02,
            error="Failed to fetch project",
            detail=str(e.orig) if e.args else "An unexpected error occurred.",
            status=500
        )

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
    try:
        service = ProjectsOpportunitiesService(session)
        filters = {
            "title": title,
            "organization": organization,
            "project_level": project_level,
            "difficulty": difficulty
        }
        projects = service.list_projects(skip=skip, limit=limit, filters=filters, sort_by=sort_by, order=order)
        logger.info(f"Listed {len(projects)} projects")
        return projects
    except Exception as e:
        logger.error(f"Error listing projects: {str(e)}")
        raise_api_error(
            code=ErrorCodes.OPPT_PROJ_DB_A03,
            error="Failed to list projects",
            detail=str(e.orig) if e.args else "An unexpected error occurred.",
            status=500
        )

@router.get("/autocomplete/", response_model=List[ReadProject])
def autocomplete_projects(
    query: str,
    field: str = Query("title"),
    limit: int = 10,
    session: Session = Depends(get_session)
):
    try:
        service = ProjectsOpportunitiesService(session)
        projects = service.autocomplete_projects(query, field, limit)
        logger.info(f"Autocomplete query '{query}' returned {len(projects)} projects")
        return projects
    except Exception as e:
        logger.error(f"Error in autocomplete for query '{query}': {str(e)}")
        raise_api_error(
            code=ErrorCodes.OPPT_PROJ_DB_A01,
            error="Failed to autocomplete projects",
            detail=str(e.orig) if e.args else "An unexpected error occurred.",
            status=500
        )

@router.put("/{project_id}", response_model=ReadProject)
def update_project(project_id: UUID, project_update: UpdateProject, session: Session = Depends(get_session)):
    try:
        service = ProjectsOpportunitiesService(session)
        project = service.update_project(project_id, project_update)
        if not project:
            logger.warning(f"Attempted update for missing project {project_id}")
            raise HTTPException(status_code=404, detail="Project not found")
        logger.info(f"Updated project {project_id}")
        return project
    except Exception as e:
        logger.error(f"Error updating project {project_id}: {str(e)}")
        raise_api_error(
            code=ErrorCodes.OPPT_PROJ_DB_A01,
            error="Failed to update project",
            detail=str(e.orig) if e.args else "An unexpected error occurred.",
            status=500
        )

@router.delete("/{project_id}", response_model=ReadProject)
def delete_project(project_id: UUID, session: Session = Depends(get_session)):
    try:
        service = ProjectsOpportunitiesService(session)
        project = service.delete_project(project_id)
        if not project:
            logger.warning(f"Attempted delete for missing project {project_id}")
            raise HTTPException(status_code=404, detail="Project not found")
        logger.info(f"Deleted project {project_id}")
        return project
    except Exception as e:
        logger.error(f"Error deleting project {project_id}: {str(e)}")
        raise_api_error(
            code=ErrorCodes.OPPT_PROJ_DB_A01,
            error="Failed to delete project",
            detail=str(e.args),
            status=e.status_code if hasattr(e, 'status_code') else 500
        )
