from typing import Optional, List, Dict, Any
from uuid import UUID
import requests
from sqlmodel import Session

from Settings.logging_config import setup_logging
from Config.constants import LEETCODE_API
from Config.queries import lc_query
from Schema.SQL.Models.models import Leetcode, LeetcodeBadges, LeetcodeTags
from Schema.SQL.Enums.enums import Tools
from Repository.User.leetcode_repository import (
    LeetcodeRepository,
    LeetcodeBadgeRepository,
    LeetcodeTagRepository,
)
from Entities.leetcode_entity import (
    CreateLeetcodeBadge,
    CreateLeetcodeTag,
    ReadLeetcodeBadge,
    ReadLeetcodeTag,
)
from Utils.error_codes import ErrorCodes
from Utils.errors import raise_api_error
from Utils.Exceptions.user_exceptions import (
    LeetcodeNotFound,
    LeetcodeBadgeNotFound,
    LeetcodeTagNotFound,
)

logger = setup_logging()


class LeetCodeService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = LeetcodeRepository(session)
        self.badge_repo = LeetcodeBadgeRepository(session)
        self.tag_repo = LeetcodeTagRepository(session)

    # Basic read helpers (kept small to align with minimal service design)
    def get(self, leetcode_id: UUID) -> Optional[Leetcode]:
        return self.repo.get(leetcode_id)

    def get_by_profile(self, profile_id: UUID) -> Optional[Leetcode]:
        return self.repo.get_by_profile_id(profile_id)

    def delete(self, leetcode_id: UUID) -> bool:
        deleted = self.repo.delete_by_id(leetcode_id)
        if not deleted:
            raise LeetcodeNotFound(leetcode_id)
        return True

    # Badge operations -------------------------------------------------
    def add_badge(self, dto: CreateLeetcodeBadge) -> LeetcodeBadges:
        badge = LeetcodeBadges(**dto.dict())
        return self.badge_repo.create(badge)

    def list_badges(self, leetcode_id: UUID) -> List[LeetcodeBadges]:
        return self.badge_repo.list(leetcode_id=leetcode_id)

    def delete_badge(self, badge_id: UUID) -> bool:
        badge = self.badge_repo.get(badge_id)
        if not badge:
            raise LeetcodeBadgeNotFound(badge_id)
        self.badge_repo.delete(badge)
        return True

    # Tag operations ---------------------------------------------------
    def add_tag(self, dto: CreateLeetcodeTag) -> LeetcodeTags:
        tag = LeetcodeTags(**dto.dict())
        return self.tag_repo.create(tag)

    def list_tags(self, leetcode_id: UUID) -> List[LeetcodeTags]:
        return self.tag_repo.list(leetcode_id=leetcode_id)

    def delete_tag(self, tag_id: UUID) -> bool:
        tag = self.tag_repo.get(tag_id)
        if not tag:
            raise LeetcodeTagNotFound(tag_id)
        self.tag_repo.delete(tag)
        return True

    def create_or_update_from_api(self, profile_id: UUID, lc_username: str) -> Leetcode:
        if not lc_username:
            raise ValueError("LeetCode username is required")
        payload = self._fetch_api(lc_username)
        if "error" in payload:
            raise_api_error(
                code=ErrorCodes.USER_LEETCODE_SRV_A02,
                error="Failed to fetch from LeetCode API",
                detail=str(payload["error"]),
                status=502,
            )

        data = payload.get("profile") or {}
        profile_node = (data.get("profile") or {})
        contest = payload.get("contestRanking") or {}

        ac_nums = (data.get("submitStatsGlobal") or {}).get("acSubmissionNum", [])
        def diff_count(name: str) -> Optional[int]:
            for item in ac_nums:
                if item.get("difficulty") == name:
                    return item.get("count")
            return None

        total = diff_count("All")
        easy = diff_count("Easy")
        medium = diff_count("Medium")
        hard = diff_count("Hard")

        raw_tags = data.get("skillTags") or []
        skill_tags: Optional[List[Tools]] = []
        for t in raw_tags:
            try:
                skill_tags.append(Tools(t))  
            except Exception:
                continue
        if not skill_tags:
            skill_tags = None

        lps = data.get("languageProblemsSolved", []) or []
        lang_counts: Optional[List[Dict[str, Any]]] = [
            {"language": x.get("language"), "problemsSolved": x.get("problemsSolved")}
            for x in lps if x.get("language")
        ] or None

        existing = self.repo.get_by_profile_id(profile_id)
        if existing:
            existing.lc_username = data.get("username")
            existing.real_name = profile_node.get("realName")
            existing.about_me = profile_node.get("aboutMe")
            existing.school = profile_node.get("school")
            existing.websites = ",".join(profile_node.get("websites", [])) if isinstance(profile_node.get("websites"), list) else profile_node.get("websites")
            existing.country = profile_node.get("countryName")
            existing.company = profile_node.get("company")
            existing.job_title = profile_node.get("jobTitle")
            existing.skill_tags = skill_tags
            existing.ranking = data.get("ranking")
            existing.avatar = profile_node.get("userAvatar") or data.get("avatar")
            existing.reputation = data.get("reputation")
            existing.solution_count = data.get("solutionCount")
            existing.total_problems_solved = total
            existing.easy_problems_solved = easy
            existing.medium_problems_solved = medium
            existing.hard_problems_solved = hard
            existing.language_problem_count = lang_counts
            existing.attended_contests = contest.get("attendedContests") or contest.get("attendedContestsCount")
            existing.competition_rating = contest.get("rating")
            existing.global_ranking = contest.get("globalRanking")
            existing.total_participants = contest.get("totalParticipants")
            existing.top_percentage = contest.get("topPercentage")
            existing.competition_badge = (contest.get("badge") or {}).get("name") if isinstance(contest.get("badge"), dict) else None
            return self.repo.update(existing)

        model = Leetcode(
            profile_id=profile_id,
            lc_username=data.get("username"),
            real_name=profile_node.get("realName"),
            about_me=profile_node.get("aboutMe"),
            school=profile_node.get("school"),
            websites=",".join(profile_node.get("websites", [])) if isinstance(profile_node.get("websites"), list) else profile_node.get("websites"),
            country=profile_node.get("countryName"),
            company=profile_node.get("company"),
            job_title=profile_node.get("jobTitle"),
            skill_tags=skill_tags,
            ranking=data.get("ranking"),
            avatar=profile_node.get("userAvatar") or data.get("avatar"),
            reputation=data.get("reputation"),
            solution_count=data.get("solutionCount"),
            total_problems_solved=total,
            easy_problems_solved=easy,
            medium_problems_solved=medium,
            hard_problems_solved=hard,
            language_problem_count=lang_counts,
            attended_contests=contest.get("attendedContests") or contest.get("attendedContestsCount"),
            competition_rating=contest.get("rating"),
            global_ranking=contest.get("globalRanking"),
            total_participants=contest.get("totalParticipants"),
            top_percentage=contest.get("topPercentage"),
            competition_badge=(contest.get("badge") or {}).get("name") if isinstance(contest.get("badge"), dict) else None,
        )
        return self.repo.create(model)

    def _fetch_api(self, username: str) -> Dict[str, Any]:
        try:
            resp = requests.post(
                LEETCODE_API,
                json={"query": lc_query, "variables": {"username": username}},
                timeout=20,
            )
            data = resp.json()
            if "errors" in data:
                return {"error": data["errors"]}
            return {
                "profile": data.get("data", {}).get("matchedUser"),
                "contestRanking": data.get("data", {}).get("userContestRanking"),
            }
        except Exception as e:  
            logger.exception("LeetCode API fetch failed")
            return {"error": str(e)}
