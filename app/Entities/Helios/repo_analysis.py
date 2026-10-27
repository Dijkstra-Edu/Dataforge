from datetime import datetime

from pydantic import BaseModel

class ProjectGradingDto(BaseModel):
    score: int
    justification: str

class RepoAnalysisDto(BaseModel):
    repo_url: str
    ai_project_grading: ProjectGradingDto 
    novelty_score: float 
    final_grade: float
    ai_summary: str
    code_quality_observation: str


class HelioRepoAnalysisResponse(BaseModel):
    exists: bool
    analysis: RepoAnalysisDto