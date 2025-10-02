from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, field_validator

from Schema.SQL.Models.models import LeetcodeTagCategory
from Schema.SQL.Enums.enums import Tools


# -------------------------------------------------------------------------
# Leetcode DTOs
# -------------------------------------------------------------------------
class CreateLeetcode(BaseModel):
    profile_id: UUID
    lc_username: Optional[str] = None
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

    @field_validator('profile_id')
    def profile_id_must_be_present(cls, v):
        if not v:
            raise ValueError('profile_id is required')
        return v

    @field_validator('lc_username')
    def lc_username_trim(cls, v):
        return v.strip() if v else v


class UpdateLeetcode(BaseModel):
    lc_username: Optional[str] = None
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

    @field_validator('lc_username')
    def lc_username_trim(cls, v):
        if v is not None and not v.strip():
            raise ValueError('lc_username cannot be empty')
        return v.strip() if v else v


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
        orm_mode = True


# -------------------------------------------------------------------------
# Leetcode Badges DTOs
# -------------------------------------------------------------------------
class CreateLeetcodeBadge(BaseModel):
    leetcode_id: UUID
    name: Optional[str] = None
    icon: Optional[str] = None
    hover_text: Optional[str] = None

    @field_validator('leetcode_id')
    def leetcode_id_must_be_present(cls, v):
        if not v:
            raise ValueError('leetcode_id is required')
        return v


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
        orm_mode = True


# -------------------------------------------------------------------------
# Leetcode Tags DTOs
# -------------------------------------------------------------------------
class CreateLeetcodeTag(BaseModel):
    leetcode_id: UUID
    tag_category: Optional[LeetcodeTagCategory] = None
    tag_name: Optional[str] = None
    problems_solved: Optional[int] = None

    @field_validator('leetcode_id')
    def leetcode_id_must_be_present(cls, v):
        if not v:
            raise ValueError('leetcode_id is required')
        return v


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
        orm_mode = True


# -------------------------------------------------------------------------
# Aggregated Read DTO including related badges & tags
# -------------------------------------------------------------------------
class ReadLeetcodeWithRelations(ReadLeetcode):
    badges: Optional[List[ReadLeetcodeBadge]] = None
    tags: Optional[List[ReadLeetcodeTag]] = None

    class Config:
        orm_mode = True
