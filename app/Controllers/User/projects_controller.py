from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlmodel import Session

from Settings.logging_config import setup_logging
from Entities.UserDTOs.projects_entity import (
    CreateProject,
    ReadProject,
    UpdateProject,
)
from Services.User.projects_service import ProjectsService
from db import get_session

logger = setup_logging()

router = APIRouter(prefix="/Dijkstra/v1/projects", tags=["Projects"])



@router.post("/", response_model=ReadProject)
def create_project(project_create: CreateProject, session: Session = Depends(get_session)):
    service = ProjectsService(session)
    logger.info(f"Creating project: {project_create.name}")
    project = service.create_project(project_create)
    logger.info(f"Created project with ID: {project.id}")
    return project


@router.get("/{project_id}", response_model=ReadProject)
def get_project(project_id: UUID, session: Session = Depends(get_session)):
    service = ProjectsService(session)
    logger.info(f"Fetching project with ID: {project_id}")
    project = service.get_project(project_id)
    logger.info(f"Fetched project with ID: {project.id}")
    return project


@router.get("/profile/{profile_id}", response_model=List[ReadProject])
def get_projects_by_profile(profile_id: UUID, session: Session = Depends(get_session)):
    service = ProjectsService(session)
    logger.info(f"Fetching projects for profile ID: {profile_id}")
    projects = service.get_projects_by_profile(profile_id)
    logger.info(f"Returned {len(projects)} projects for profile {profile_id}")
    return projects


@router.get("/", response_model=List[ReadProject])
def list_projects(skip: int = 0, limit: int = 20, session: Session = Depends(get_session)):
    service = ProjectsService(session)
    logger.info(f"Listing projects: skip={skip}, limit={limit}")
    projects = service.list_projects(skip=skip, limit=limit)
    logger.info(f"Returned {len(projects)} projects")
    return projects


@router.put("/{project_id}", response_model=ReadProject)
def update_project(project_id: UUID, project_update: UpdateProject, session: Session = Depends(get_session)):
    service = ProjectsService(session)
    logger.info(f"Updating project ID: {project_id}")
    project = service.update_project(project_id, project_update)
    logger.info(f"Updated project ID: {project.id}")
    return project


@router.delete("/{project_id}")
def delete_project(project_id: UUID, session: Session = Depends(get_session)):
    service = ProjectsService(session)
    logger.info(f"Deleting project ID: {project_id}")
    message = service.delete_project(project_id)
    logger.info(f"Deleted project ID: {project_id}")
    return {"detail": message}
