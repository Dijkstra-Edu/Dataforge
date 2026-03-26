from typing import Any, List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from Settings.logging_config import get_logger
from Services.User.skills_service import SkillsService
from db import get_session

logger = get_logger()

router = APIRouter(prefix="/Dijkstra/v1/skills", tags=["Skills"])

@router.get("/{github_username}", response_model=List[Any])
def get_skills_by_github_username(github_username: str, session: Session = Depends(get_session)):
    service = SkillsService(session)
    logger.info(f"Fetching Skills for GitHub username: {github_username}")
    skills = service.get_skills_by_github_username(github_username)
    return skills

    