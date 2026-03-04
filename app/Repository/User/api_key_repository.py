from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError

from Schema.SQL.Models.models import APIKey

class APIKeyRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, api_key: APIKey) -> APIKey:
        try:
            self.session.add(api_key)
            self.session.commit()
            self.session.refresh(api_key)
            return api_key
        except SQLAlchemyError as e:
            self.session.rollback()
            raise

    def get_by_key_hash(self, key_hash: str) -> Optional[APIKey]:
        statement = select(APIKey).where(APIKey.key_hash == key_hash)
        return self.session.exec(statement).first()

    def get_by_id(self, api_key_id: UUID) -> Optional[APIKey]:
        statement = select(APIKey).where(APIKey.id == api_key_id)
        return self.session.exec(statement).first()

    def list_by_github_username(self, github_username: str) -> List[APIKey]:
        statement = select(APIKey).where(APIKey.github_username == github_username)
        return self.session.exec(statement).all()

    def update(self, api_key: APIKey) -> APIKey:
        try:
            self.session.add(api_key)
            self.session.commit()
            self.session.refresh(api_key)
            return api_key
        except SQLAlchemyError as e:
            self.session.rollback()
            raise

    def revoke(self, api_key_id: UUID) -> None:
        try:
            api_key = self.get_by_id(api_key_id)
            if api_key:
                api_key.active = False
                self.session.add(api_key)
                self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise

    def get_active_by_key_hash(self, key_hash: str) -> Optional[APIKey]:
        """Get active, non-expired API key by hash."""
        statement = (
            select(APIKey)
            .where(APIKey.key_hash == key_hash)
            .where(APIKey.active == True)
        )
        api_key = self.session.exec(statement).first()
        
        if api_key and api_key.expires_in:
            if api_key.expires_in < datetime.now(timezone.utc):
                return None  # Expired
        
        return api_key

