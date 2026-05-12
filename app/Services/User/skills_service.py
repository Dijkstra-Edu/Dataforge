from typing import List
from sqlmodel import Session
from Schema.SQL.Models.models import Skills

class SkillsService:
    def __init__(self, session: Session):
        self.session = session

    def get_skills_by_github_username(self, github_username: str) -> List[Skills]:
        return self.compute_skills(github_username)

    def compute_skills(self, github_username: str) -> List[Skills]:
        return []