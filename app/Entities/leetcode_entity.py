from typing import List, Optional, Annotated
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

from Schema.SQL.Models.models import LeetcodeTagCategory
from Schema.SQL.Enums.enums import Tools


# -------------------------------------------------------------------------
# Leetcode DTOs
# -------------------------------------------------------------------------
class CreateLeetcode(BaseModel):
    profile_id: UUID
    lc_username: Optional[Annotated[str, Field(min_length=1, strip_whitespace=True)]] = None
    real_name: Optional[str] = None
    about_me: Optional[str] = None
    school: Optional[str] = None
    websites: Optional[str] = None
    country: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    skill_tags: Optional[List[Tools]] = None
    ranking: Optional[int] = None
    avatar: Optional[str] = None
    reputation: Optional[int] = None
    solution_count: Optional[int] = None
    total_problems_solved: Optional[int] = None
    easy_problems_solved: Optional[int] = None
    medium_problems_solved: Optional[int] = None
    hard_problems_solved: Optional[int] = None
    language_problem_count: Optional[List[str]] = None
    attended_contests: Optional[int] = None
    competition_rating: Optional[float] = None
    global_ranking: Optional[int] = None
    total_participants: Optional[int] = None
    top_percentage: Optional[float] = None
    competition_badge: Optional[str] = None


class UpdateLeetcode(BaseModel):
    lc_username: Optional[Annotated[str, Field(min_length=1, strip_whitespace=True)]] = None
    real_name: Optional[str] = None
    about_me: Optional[str] = None
    school: Optional[str] = None
    websites: Optional[str] = None
    country: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    skill_tags: Optional[List[Tools]] = None
    ranking: Optional[int] = None
    avatar: Optional[str] = None
    reputation: Optional[int] = None
    solution_count: Optional[int] = None
    total_problems_solved: Optional[int] = None
    easy_problems_solved: Optional[int] = None
    medium_problems_solved: Optional[int] = None
    hard_problems_solved: Optional[int] = None
    language_problem_count: Optional[List[str]] = None
    attended_contests: Optional[int] = None
    competition_rating: Optional[float] = None
    global_ranking: Optional[int] = None
    total_participants: Optional[int] = None
    top_percentage: Optional[float] = None
    competition_badge: Optional[str] = None


class ReadLeetcode(BaseModel):
    id: UUID
    profile_id: UUID
    lc_username: Optional[str]
    real_name: Optional[str]
    about_me: Optional[str]
    school: Optional[str]
    websites: Optional[str]
    country: Optional[str]
    company: Optional[str]
    job_title: Optional[str]
    skill_tags: Optional[List[Tools]]
    ranking: Optional[int]
    avatar: Optional[str]
    reputation: Optional[int]
    solution_count: Optional[int]
    total_problems_solved: Optional[int]
    easy_problems_solved: Optional[int]
    medium_problems_solved: Optional[int]
    hard_problems_solved: Optional[int]
    language_problem_count: Optional[List[str]]
    attended_contests: Optional[int]
    competition_rating: Optional[float]
    global_ranking: Optional[int]
    total_participants: Optional[int]
    top_percentage: Optional[float]
    competition_badge: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# -------------------------------------------------------------------------
# Leetcode Badges DTOs
# -------------------------------------------------------------------------
class CreateLeetcodeBadge(BaseModel):
    leetcode_id: UUID
    name: Optional[str] = None
    icon: Optional[str] = None
    hover_text: Optional[str] = None


class UpdateLeetcodeBadge(BaseModel):
    name: Optional[str] = None
    icon: Optional[str] = None
    hover_text: Optional[str] = None


class ReadLeetcodeBadge(BaseModel):
    id: UUID
    leetcode_id: UUID
    name: Optional[str]
    icon: Optional[str]
    hover_text: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# -------------------------------------------------------------------------
# Leetcode Tags DTOs
# -------------------------------------------------------------------------
class CreateLeetcodeTag(BaseModel):
    leetcode_id: UUID
    tag_category: Optional[LeetcodeTagCategory] = None
    tag_name: Optional[str] = None
    problems_solved: Optional[int] = None


class UpdateLeetcodeTag(BaseModel):
    tag_category: Optional[LeetcodeTagCategory] = None
    tag_name: Optional[str] = None
    problems_solved: Optional[int] = None


class ReadLeetcodeTag(BaseModel):
    id: UUID
    leetcode_id: UUID
    tag_category: Optional[LeetcodeTagCategory]
    tag_name: Optional[str]
    problems_solved: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# -------------------------------------------------------------------------
# Aggregated Read DTO including related badges & tags
# -------------------------------------------------------------------------
class ReadLeetcodeWithRelations(ReadLeetcode):
    badges: Optional[List[ReadLeetcodeBadge]] = None
    tags: Optional[List[ReadLeetcodeTag]] = None

    class Config:
        from_attributes = True
