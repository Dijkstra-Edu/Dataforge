from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session

from db import get_session
from Settings.logging_config import setup_logging
from Services.User.leetcode_service import LeetCodeService
from Entities.leetcode_entity import (
    ReadLeetcode,
    CreateLeetcodeBadge,
    CreateLeetcodeTag,
    ReadLeetcodeBadge,
    ReadLeetcodeTag,
)

logger = setup_logging()

router = APIRouter(prefix="/Dijkstra/v1/leetcode", tags=["Leetcode"])


@router.post("/sync/{profile_id}/{lc_username}", response_model=ReadLeetcode)
def sync_leetcode(profile_id: UUID, lc_username: str, session: Session = Depends(get_session)):
    service = LeetCodeService(session)
    logger.info(f"Syncing LeetCode data profile_id={profile_id} username={lc_username}")
    return service.create_or_update_from_api(profile_id, lc_username)


@router.get("/{leetcode_id}", response_model=ReadLeetcode)
def get_leetcode(leetcode_id: UUID, session: Session = Depends(get_session)):
    service = LeetCodeService(session)
    model = service.get(leetcode_id)
    if not model:
        raise HTTPException(status_code=404, detail="LeetCode record not found")
    return model


@router.get("/profile/{profile_id}", response_model=ReadLeetcode)
def get_leetcode_by_profile(profile_id: UUID, session: Session = Depends(get_session)):
    service = LeetCodeService(session)
    model = service.get_by_profile(profile_id)
    if not model:
        raise HTTPException(status_code=404, detail="LeetCode record not found for profile")
    return model


@router.delete("/{leetcode_id}", status_code=204)
def delete_leetcode(leetcode_id: UUID, session: Session = Depends(get_session)):
    service = LeetCodeService(session)
    service.delete(leetcode_id)
    return Response(status_code=204)


# ----------------------------- Badges ---------------------------------
@router.post("/{leetcode_id}/badges", response_model=ReadLeetcodeBadge)
def create_badge(leetcode_id: UUID, payload: CreateLeetcodeBadge, session: Session = Depends(get_session)):
    if payload.leetcode_id != leetcode_id:
        raise HTTPException(status_code=400, detail="leetcode_id mismatch")
    service = LeetCodeService(session)
    return service.add_badge(payload)


@router.get("/{leetcode_id}/badges", response_model=list[ReadLeetcodeBadge])
def list_badges(leetcode_id: UUID, session: Session = Depends(get_session)):
    service = LeetCodeService(session)
    return service.list_badges(leetcode_id)


@router.delete("/badges/{badge_id}", status_code=204)
def delete_badge(badge_id: UUID, session: Session = Depends(get_session)):
    service = LeetCodeService(session)
    service.delete_badge(badge_id)
    return Response(status_code=204)


# ----------------------------- Tags -----------------------------------
@router.post("/{leetcode_id}/tags", response_model=ReadLeetcodeTag)
def create_tag(leetcode_id: UUID, payload: CreateLeetcodeTag, session: Session = Depends(get_session)):
    if payload.leetcode_id != leetcode_id:
        raise HTTPException(status_code=400, detail="leetcode_id mismatch")
    service = LeetCodeService(session)
    return service.add_tag(payload)


@router.get("/{leetcode_id}/tags", response_model=list[ReadLeetcodeTag])
def list_tags(leetcode_id: UUID, session: Session = Depends(get_session)):
    service = LeetCodeService(session)
    return service.list_tags(leetcode_id)


@router.delete("/tags/{tag_id}", status_code=204)
def delete_tag(tag_id: UUID, session: Session = Depends(get_session)):
    service = LeetCodeService(session)
    service.delete_tag(tag_id)
    return Response(status_code=204)
