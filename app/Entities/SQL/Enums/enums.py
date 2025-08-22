from typing import List, Optional, Union
from datetime import date, datetime
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from pydantic import BaseModel
from typing_extensions import Annotated
from uuid import UUID, uuid4

# Enums for USER-DEFINED types
class CertificationType(str, Enum):
    PROFESSIONAL = "professional"
    ACADEMIC = "academic"
    COURSE = "course"
    # Add other types as needed

class Currency(str, Enum):
    INR = "INR"
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    CHF = "CHF"
    AUD = "AUD"
    SGD = "SGD"
    # Add other currencies as needed

class SchoolType(str, Enum):
    UNIVERSITY = "university"
    COLLEGE = "college"
    SCHOOL = "school"
    ONLINE = "online"
    # Add other types as needed

class LocationType(str, Enum):
    PHYSICAL = "physical"
    REMOTE = "remote"
    HYBRID = "hybrid"

class EmploymentType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    FREELANCE = "freelance"

class Rank(str, Enum):
    UNRANKED = "unranked"
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"

class Difficulty(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"