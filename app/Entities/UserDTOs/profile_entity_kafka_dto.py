from pydantic import BaseModel
from typing import Optional, List, Dict
from Schema.SQL.Models.models import Profile
from sqlalchemy import null

from Schema.SQL.Enums.enums import SchoolType
from Utils.utility_functions import calculate_months_served
from Services.User.statistics_service import StatisticsService


class EducationUpdateEventDTO(BaseModel):
    """Education Update Event DTO"""
    salary: int
    time_served_months: int

class CpgaUpdateEventDTO(BaseModel):
    """CPGA Update Event DTO"""
    cgpa: float

class DsaMetricsUpdateEventDTO(BaseModel):
    """Dsa Metrics Update Event DTO"""
    contest_rating: int
    global_rank: int

class ProfileUpdateKafkaEvent(BaseModel):
    """Kafka event payload for profile updates"""
    user_id: str
    work_experiences: Optional[List[EducationUpdateEventDTO]] = None
    cgpa_metrics: Optional[CpgaUpdateEventDTO] = None
    dsa_metrics: Optional[DsaMetricsUpdateEventDTO] = None

def map_profile_to_kafka_event(profile: Profile) -> ProfileUpdateKafkaEvent:
    """
    Convert a Profile ORM object into a ProfileUpdateKafkaEvent DTO.
    """

    # ----------------------------
    # Work Experiences Mapping
    # ----------------------------
    work_experience_dtos = []
    for wx in profile.work_experience:
        months_served = calculate_months_served(
            wx.start_date_month,
            wx.start_date_year,
            wx.end_date_month,
            wx.end_date_year
        )
        work_experience_dtos.append(
            EducationUpdateEventDTO(
                salary=(wx.yearly_salary_rupees or 2000000) / 100000, #TODO: This should be 0. Have kept it to a large number for dev testing since frontend does not possess this field.
                time_served_months=months_served,
            )
        )
    # ----------------------------
    # CGPA Mapping
    # ----------------------------
    edu = next(
        (e for e in profile.education
         if e.school_type in {SchoolType.UNIVERSITY, SchoolType.COLLEGE}),
        None
    )
    #FIXME: Currently the CGPA is in the 4 scale while helios expects the 10 scale. This needs to be fixed from the frontend
    cgpa_dto = CpgaUpdateEventDTO(cgpa=edu.cgpa) if edu and edu.cgpa is not None else None

    # ----------------------------
    # DSA Metrics Mapping
    # ----------------------------
    # leetcode_profile = profile.leetcode
    leetcode_username = (
        profile.user_rel
        and profile.user_rel.links
        and profile.user_rel.links.leetcode_user_name
    )
    leetcode_statistics = StatisticsService.getAllLeetcodeData(leetcode_username) if leetcode_username else None
    print("Leetcode statistics: " + str(leetcode_statistics["leetcode"]["profile"]) if leetcode_statistics else "No LeetCode data")
    dsa_dto = DsaMetricsUpdateEventDTO(
        contest_rating=int(leetcode_statistics["leetcode"]["contestRanking"]["rating"]) if leetcode_statistics else 0,
        global_rank=int(leetcode_statistics["leetcode"]["profile"]["profile"]["ranking"]) if leetcode_statistics else 0
    ) if leetcode_statistics else None

    # ----------------------------
    # Construct final event DTO
    # ----------------------------
    event = ProfileUpdateKafkaEvent(
        user_id=str(profile.user_rel.github_user_name),
        work_experiences=work_experience_dtos,
        cgpa_metrics=cgpa_dto,
        dsa_metrics=dsa_dto,
    )

    return event