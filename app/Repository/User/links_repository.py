from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from sqlalchemy import asc, desc
from sqlalchemy.exc import SQLAlchemyError

from Schema.SQL.Models.models import Links


class LinksRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, link: Links) -> Links:
        try:
            self.session.add(link)
            self.session.commit()
            self.session.refresh(link)
            return link
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def get(self, link_id: UUID) -> Optional[Links]:
        statement = select(Links).where(Links.id == link_id)
        return self.session.exec(statement).first()

    def get_by_user_id(self, user_id: UUID) -> Optional[Links]:
        statement = select(Links).where(Links.user_id == user_id)
        return self.session.exec(statement).first()

    def list(
        self,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        order: str = "desc",
        github_user_name: Optional[str] = None,
        linkedin_user_name: Optional[str] = None,
        leetcode_user_name: Optional[str] = None,
        orcid_id: Optional[str] = None,
        primary_email: Optional[str] = None,
        secondary_email: Optional[str] = None,
        school_email: Optional[str] = None,
        work_email: Optional[str] = None,
    ) -> List[Links]:
        """
        List links with pagination, filtering, and sorting.
        """

        statement = select(Links)

        # Filtering
        if github_user_name:
            statement = statement.where(Links.github_user_name.ilike(f"%{github_user_name}%"))
        if linkedin_user_name:
            statement = statement.where(Links.linkedin_user_name.ilike(f"%{linkedin_user_name}%"))
        if leetcode_user_name:
            statement = statement.where(Links.leetcode_user_name.ilike(f"%{leetcode_user_name}%"))
        if orcid_id:
            statement = statement.where(Links.orcid_id.ilike(f"%{orcid_id}%"))
        if primary_email:
            statement = statement.where(Links.primary_email.ilike(f"%{primary_email}%"))
        if secondary_email:
            statement = statement.where(Links.secondary_email.ilike(f"%{secondary_email}%"))
        if school_email:
            statement = statement.where(Links.school_email.ilike(f"%{school_email}%"))
        if work_email:
            statement = statement.where(Links.work_email.ilike(f"%{work_email}%"))


        # Sorting
        sort_column = getattr(Links, sort_by, Links.created_at)  # default: created_at
        if order.lower() == "desc":
            statement = statement.order_by(desc(sort_column))
        else:
            statement = statement.order_by(asc(sort_column))

        # Pagination
        statement = statement.offset(skip).limit(limit)

        return self.session.exec(statement).all()

    def update(self, link: Links) -> Links:
        try:
            self.session.add(link)
            self.session.commit()
            self.session.refresh(link)
            return link
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def delete(self, link: Links) -> None:
        try:
            self.session.delete(link)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise
