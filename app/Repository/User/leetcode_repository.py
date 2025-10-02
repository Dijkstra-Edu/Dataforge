from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from sqlalchemy import asc, desc
from sqlalchemy.exc import SQLAlchemyError

from Schema.SQL.Models.models import Leetcode, LeetcodeBadges, LeetcodeTags, LeetcodeTagCategory


class LeetcodeRepository:
    def __init__(self, session: Session):
        self.session = session

    # ------------------------------------------------------------------
    # Core Leetcode
    # ------------------------------------------------------------------
    def create(self, leetcode: Leetcode) -> Leetcode:
        try:
            self.session.add(leetcode)
            self.session.commit()
            self.session.refresh(leetcode)
            return leetcode
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def get(self, leetcode_id: UUID) -> Optional[Leetcode]:
        statement = select(Leetcode).where(Leetcode.id == leetcode_id)
        return self.session.exec(statement).first()

    def get_by_profile_id(self, profile_id: UUID) -> Optional[Leetcode]:
        statement = select(Leetcode).where(Leetcode.profile_id == profile_id)
        return self.session.exec(statement).first()

    def get_by_username(self, lc_username: str) -> Optional[Leetcode]:
        statement = select(Leetcode).where(Leetcode.lc_username == lc_username)
        return self.session.exec(statement).first()

    def list(
        self,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        order: str = "desc",
        profile_id: Optional[UUID] = None,
        lc_username: Optional[str] = None,
        country: Optional[str] = None,
        company: Optional[str] = None,
        min_total_solved: Optional[int] = None,
        max_total_solved: Optional[int] = None,
        min_rating: Optional[float] = None,
        max_rating: Optional[float] = None,
    ) -> List[Leetcode]:
        statement = select(Leetcode)

        # Filtering
        if profile_id:
            statement = statement.where(Leetcode.profile_id == profile_id)
        if lc_username:
            statement = statement.where(Leetcode.lc_username.ilike(f"%{lc_username}%"))
        if country:
            statement = statement.where(Leetcode.country.ilike(f"%{country}%"))
        if company:
            statement = statement.where(Leetcode.company.ilike(f"%{company}%"))
        if min_total_solved is not None:
            statement = statement.where(Leetcode.total_problems_solved >= min_total_solved)
        if max_total_solved is not None:
            statement = statement.where(Leetcode.total_problems_solved <= max_total_solved)
        if min_rating is not None:
            statement = statement.where(Leetcode.competition_rating >= min_rating)
        if max_rating is not None:
            statement = statement.where(Leetcode.competition_rating <= max_rating)

        # Sorting
        sort_column = getattr(Leetcode, sort_by, Leetcode.created_at)
        if order.lower() == "desc":
            statement = statement.order_by(desc(sort_column))
        else:
            statement = statement.order_by(asc(sort_column))

        # Pagination
        statement = statement.offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def update(self, leetcode: Leetcode) -> Leetcode:
        try:
            self.session.add(leetcode)
            self.session.commit()
            self.session.refresh(leetcode)
            return leetcode
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def delete(self, leetcode: Leetcode):
        try:
            self.session.delete(leetcode)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def delete_by_id(self, leetcode_id: UUID) -> bool:
        """Delete a Leetcode record by its ID. Returns True if deleted, False if not found."""
        record = self.get(leetcode_id)
        if not record:
            return False
        self.delete(record)
        return True


# ------------------------------------------------------------------
# Badge Repository
# ------------------------------------------------------------------
class LeetcodeBadgeRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, badge: LeetcodeBadges) -> LeetcodeBadges:
        try:
            self.session.add(badge)
            self.session.commit()
            self.session.refresh(badge)
            return badge
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def get(self, badge_id: UUID) -> Optional[LeetcodeBadges]:
        statement = select(LeetcodeBadges).where(LeetcodeBadges.id == badge_id)
        return self.session.exec(statement).first()

    def list(
        self,
        leetcode_id: Optional[UUID] = None,
        name: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
        sort_by: str = "created_at",
        order: str = "desc",
    ) -> List[LeetcodeBadges]:
        statement = select(LeetcodeBadges)
        if leetcode_id:
            statement = statement.where(LeetcodeBadges.leetcode_id == leetcode_id)
        if name:
            statement = statement.where(LeetcodeBadges.name.ilike(f"%{name}%"))

        sort_column = getattr(LeetcodeBadges, sort_by, LeetcodeBadges.created_at)
        if order.lower() == "desc":
            statement = statement.order_by(desc(sort_column))
        else:
            statement = statement.order_by(asc(sort_column))
        statement = statement.offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def update(self, badge: LeetcodeBadges) -> LeetcodeBadges:
        try:
            self.session.add(badge)
            self.session.commit()
            self.session.refresh(badge)
            return badge
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def delete(self, badge: LeetcodeBadges):
        try:
            self.session.delete(badge)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise


# ------------------------------------------------------------------
# Tag Repository
# ------------------------------------------------------------------
class LeetcodeTagRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, tag: LeetcodeTags) -> LeetcodeTags:
        try:
            self.session.add(tag)
            self.session.commit()
            self.session.refresh(tag)
            return tag
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def get(self, tag_id: UUID) -> Optional[LeetcodeTags]:
        statement = select(LeetcodeTags).where(LeetcodeTags.id == tag_id)
        return self.session.exec(statement).first()

    def list(
        self,
        leetcode_id: Optional[UUID] = None,
        tag_category: Optional[LeetcodeTagCategory] = None,
        tag_name: Optional[str] = None,
        min_solved: Optional[int] = None,
        max_solved: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "created_at",
        order: str = "desc",
    ) -> List[LeetcodeTags]:
        statement = select(LeetcodeTags)
        if leetcode_id:
            statement = statement.where(LeetcodeTags.leetcode_id == leetcode_id)
        if tag_category:
            statement = statement.where(LeetcodeTags.tag_category == tag_category)
        if tag_name:
            statement = statement.where(LeetcodeTags.tag_name.ilike(f"%{tag_name}%"))
        if min_solved is not None:
            statement = statement.where(LeetcodeTags.problems_solved >= min_solved)
        if max_solved is not None:
            statement = statement.where(LeetcodeTags.problems_solved <= max_solved)

        sort_column = getattr(LeetcodeTags, sort_by, LeetcodeTags.created_at)
        statement = statement.order_by(desc(sort_column) if order.lower() == "desc" else asc(sort_column))
        statement = statement.offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def update(self, tag: LeetcodeTags) -> LeetcodeTags:
        try:
            self.session.add(tag)
            self.session.commit()
            self.session.refresh(tag)
            return tag
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def delete(self, tag: LeetcodeTags):
        try:
            self.session.delete(tag)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise
