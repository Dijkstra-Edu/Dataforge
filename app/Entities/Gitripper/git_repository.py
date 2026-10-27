from datetime import datetime

from pydantic import BaseModel


class GitRepoStats(BaseModel):
    owner: str
    name: str
    stars: int
    forks: int 
    lastUpdatedAt: datetime
    issuesCount: int
    ownerLineContribution: int