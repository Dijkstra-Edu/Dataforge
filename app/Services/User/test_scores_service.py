from Settings.logging_config import setup_logging
from uuid import UUID
from typing import List, Optional
from sqlmodel import Session
from Repository.User.test_scores_repository import TestScoresRepository
from Schema.SQL.Models.models import TestScores
from Utils.Exceptions.user_exceptions import TestScoreNotFound
from Entities.UserDTOs.test_scores_entity import CreateTestScore, UpdateTestScore

logger = setup_logging()

class TestScoresService:
       
        def __init__(self, session: Session):
            self.repo = TestScoresRepository(session)
            self.session = session
        
        def create_test_score(self, test_score_create: CreateTestScore):
            test_score = TestScores(**test_score_create.dict(exclude_unset=True))
            return self.repo.create(test_score)
        
        def list_all_test_scores(self, skip: int = 0, limit: int = 20, sort_by: str = "created_at", title: Optional[str] = None, order: str = "desc", user_id: Optional[UUID] = None) -> List[TestScores]:
            test_scores = self.repo.list(skip=skip, limit=limit, sort_by=sort_by, order=order, user_id=user_id, title=title)
            if not test_scores:
                raise TestScoreNotFound()
            return test_scores
        
        def get_test_score(self, test_score_id: UUID) -> Optional[TestScores]:
            test_score = self.repo.get(test_score_id)
            if not test_score:
                raise TestScoreNotFound(test_score_id)
            return test_score
        
        def update_test_score(self, test_score_id: UUID, test_score_update: UpdateTestScore):
            test_score = self.repo.get(test_score_id)
            if not test_score:
                raise TestScoreNotFound(test_score_id)
            
            update_data = test_score_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(test_score, key, value)
            return self.repo.update(test_score)
        
        def delete_test_score(self, test_score_id: UUID) -> Optional[str]:
            test_score = self.repo.get(test_score_id)
            if not test_score:
                raise TestScoreNotFound(test_score_id)
            self.repo.delete(test_score)
            return f"Test score {test_score_id} deleted successfully."
        
        def get_test_scores_by_profile(self, profile_id: UUID) -> List[TestScores]:
            """
            Get all test scores for a specific profile.
            Returns empty list if no test scores found.
            """
            test_scores = self.repo.get_by_profile_id(profile_id)
            return test_scores if test_scores else []
        
        def get_test_scores_by_github_username(self, github_username: str) -> List[TestScores]:
            """Get all test scores by GitHub username"""
            from Services.User.profile_service import ProfileService
            
            profile_service = ProfileService(self.session)
            profile_id = profile_service.get_profile_id_by_github_username(github_username)
            return self.get_test_scores_by_profile(profile_id)
