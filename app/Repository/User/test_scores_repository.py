from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from sqlalchemy import asc, desc
from sqlalchemy.exc import SQLAlchemyError
from Schema.SQL.Models.models import TestScores, Profile, User

class TestScoresRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, test_score: TestScores) -> TestScores:
        try:
            self.session.add(test_score)
            self.session.commit()
            self.session.refresh(test_score)
            return test_score
        except SQLAlchemyError as e:
            self.session.rollback()
            raise
        
    def list(
        self,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        order: str = "desc",
        title: Optional[str] = None,
        user_id: Optional[UUID] = None,
    ) -> List[TestScores]:

        statement = select(TestScores)

        if user_id:
            statement = (
                statement.join(Profile, Profile.id == TestScores.profile_id)
                .join(User, User.id == Profile.user_id)
                .where(User.id == user_id)
            )

        if title:
            title = title.strip()
            if title:
                statement = statement.where(
                    TestScores.title.ilike(f"%{title}%")
                )

        # Sorting (fallback to created_at if invalid)
        sort_column = getattr(TestScores, sort_by, TestScores.created_at)
        if order.lower() == "desc":
            statement = statement.order_by(desc(sort_column))
        else:
            statement = statement.order_by(asc(sort_column))

        # Pagination
        statement = statement.offset(skip).limit(limit)

        return self.session.exec(statement).all()
        
    def get(self, test_score_id: UUID) -> Optional[TestScores]:
        statement = select(TestScores).where(TestScores.id == test_score_id)
        return self.session.exec(statement).first()
    
    def update(self, test_score: TestScores) -> TestScores:
        try:
            self.session.add(test_score)
            self.session.commit()
            self.session.refresh(test_score)
            return test_score
        except SQLAlchemyError:
            self.session.rollback()
            raise
    
    def delete(self, test_score: TestScores):
        try:
            self.session.delete(test_score)
            self.session.commit()
        except SQLAlchemyError:
            raise
    
    def get_by_profile_id(self, profile_id: UUID) -> List[TestScores]:
        """Get all test scores for a specific profile."""
        statement = select(TestScores).where(TestScores.profile_id == profile_id)
        return self.session.exec(statement).all()
