from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from uuid import UUID

from sqlmodel import Session
from Settings.logging_config import setup_logging
from Services.User.test_scores_service import TestScoresService
from Entities.UserDTOs.test_scores_entity import CreateTestScore, UpdateTestScore, ReadTestScore
from db import get_session
logger = setup_logging()

router = APIRouter(prefix="/Dijkstra/v1/test-scores", tags=["Test Scores"])

@router.post("/", response_model=ReadTestScore)
def create_test_score(test_score_create: CreateTestScore, session: Session = Depends(get_session)):
    service = TestScoresService(session)
    logger.info(f"Creating Test Score: {test_score_create.title}")
    test_score = service.create_test_score(test_score_create)
    logger.info(f"Created Test Score with ID: {test_score.id}")
    return test_score

@router.get("/", response_model=List[ReadTestScore])
def list_test_scores(
    skip: int = 0,
    limit: int = 20,
    sort_by: str = Query("created_at", description="Field to be sorted by"),
    order: str = Query("desc", description="asc or desc"),
    title: Optional[str] = None,
    session: Session = Depends(get_session)
):
    service = TestScoresService(session)
    logger.info(f"Fetching all test scores: skip={skip}, limit={limit}, sort_by={sort_by}, order={order}, title={title}")
    test_scores = service.list_all_test_scores(skip=skip, limit=limit, sort_by=sort_by, order=order, title=title)
    return test_scores

@router.get("/id/{test_score_id}", response_model=ReadTestScore)
def get_test_score(test_score_id: UUID, session: Session = Depends(get_session)):
    service = TestScoresService(session)
    logger.info(f"Fetching Test Score with ID: {test_score_id}")
    test_score = service.get_test_score(test_score_id)
    return test_score

@router.get("/{github_username}", response_model=List[ReadTestScore])
def get_test_scores_by_github_username(github_username: str, session: Session = Depends(get_session)):
    service = TestScoresService(session)
    logger.info(f"Fetching Test Scores for GitHub username: {github_username}")
    test_scores = service.get_test_scores_by_github_username(github_username)
    return test_scores

@router.put("/{test_score_id}", response_model=ReadTestScore)
def update_test_score(test_score_id: UUID, test_score_update: UpdateTestScore, session: Session = Depends(get_session)):
    service = TestScoresService(session)
    logger.info(f"Updating Test Score ID: {test_score_id} with data {test_score_update.dict(exclude_unset=True)}")
    test_score = service.update_test_score(test_score_id, test_score_update)
    logger.info(f"Updated Test Score with ID: {test_score.id}")
    return test_score

@router.delete("/{test_score_id}", response_model=ReadTestScore)
def delete_test_score(test_score_id: UUID, session: Session = Depends(get_session)):
    service = TestScoresService(session)
    logger.info(f"Delete Test Score with ID: {test_score_id}")
    test_score = service.get_test_score(test_score_id)
    message = service.delete_test_score(test_score_id)
    logger.info(message)
    return test_score
