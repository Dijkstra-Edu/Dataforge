from typing import List, Optional
from datetime import date, datetime, timezone

from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from Entities.SQL.Enums.enums import Difficulty, ProjectLevel, Rank, Tools, WorkLocationType, EmploymentType, Currency
from sqlalchemy import ARRAY, Column, Enum as SQLEnum, String

# Base class with UUID PK and timestamps
class UUIDBaseTable(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": datetime.now(timezone.utc)}
    )

# -------------------------------------------------------------------------
# Organization model
# -------------------------------------------------------------------------
class Organization(UUIDBaseTable, table=True):
    __tablename__ = "Organizations"

    name: Optional[str] = None
    image: Optional[str] = None
    repo_link: Optional[str] = None

    # Relationships
    jobs: List["Job"] = Relationship(back_populates="organization_rel")
    projects: List["ProjectsOpportunities"] = Relationship(
        back_populates="organization_rel"
    )
    fellowships: List["Fellowship"] = Relationship(
        back_populates="organization_rel"
    )


# -------------------------------------------------------------------------
# Job model
# -------------------------------------------------------------------------
class Job(UUIDBaseTable, table=True):
    __tablename__ = "Jobs"

    title: Optional[str] = None
    department: Optional[str] = None
    company_name: Optional[str] = None
    company_logo: Optional[str] = None
    hero_image: Optional[str] = None
    location: Optional[str] = None
    location_type: Optional[WorkLocationType] = Field(
        sa_column=Column(SQLEnum(WorkLocationType, name="WORK_LOCATION_TYPE"))
    )
    employment_type: Optional[EmploymentType] = Field(
        sa_column=Column(SQLEnum(EmploymentType, name="EMPLOYMENT_TYPE"))
    )
    experience_level: Optional[str] = None
    experience_yoe: Optional[float] = None
    posted_date: Optional[date] = None
    salary_annual_min: Optional[int] = None
    salary_annual_max: Optional[int] = None
    salary_currency: Optional[Currency] = Field(
        sa_column=Column(SQLEnum(Currency, name="CURRENCY"))
    )
    description: Optional[str] = None
    featured: Optional[bool] = None
    highlight: Optional[str] = None
    category: Optional[str] = None
    perks: Optional[List[str]] = Field(
        default_factory=list, sa_column=Column(ARRAY(String))
    )

    # Foreign key to Organization
    organization: Optional[UUID] = Field(
        default=None, foreign_key="Organizations.id", nullable=True
    )
    organization_rel: Optional[Organization] = Relationship(back_populates="jobs")


# -------------------------------------------------------------------------
# Projects Opportunities model
# -------------------------------------------------------------------------
class ProjectsOpportunities(UUIDBaseTable, table=True):
    __tablename__ = "ProjectsOpportunities"

    title: Optional[str] = None
    project_level: Optional[ProjectLevel] = Field(
        sa_column=Column(SQLEnum(ProjectLevel, name="PROJECT_LEVEL"))
    )
    is_user_project: Optional[bool] = None
    owner: Optional[str] = None
    organization: Optional[UUID] = Field(
        default=None, foreign_key="Organizations.id", nullable=True
    )
    organization_logo: Optional[str] = None
    hero_image: Optional[str] = None
    repository: Optional[str] = None

    # languages & frameworks (USER-DEFINED in schema, but let's treat as TEXT ARRAY for flexibility)
    languages: Optional[List[str]] = Field(
        sa_column=Column(ARRAY(SQLEnum(Tools, name="TOOLS_ENUM")))
    )
    frameworks: Optional[List[str]] = Field(
        sa_column=Column(ARRAY(SQLEnum(Tools, name="TOOLS_ENUM")))
    )

    stars: Optional[int] = None
    forks: Optional[int] = None
    last_updated: Optional[date] = None
    description: Optional[str] = None
    featured: Optional[bool] = None
    highlight: Optional[str] = None
    category: Optional[List[str]] = Field(
        default_factory=list, sa_column=Column(ARRAY(String))
    )
    difficulty: Optional[Difficulty] = Field(
        sa_column=Column(SQLEnum(Difficulty, name="DIFFICULTY"))
    )
    issues_count: Optional[int] = None
    contributors_count: Optional[int] = None
    license: Optional[str] = None
    topics: Optional[List[str]] = Field(
        default_factory=list, sa_column=Column(ARRAY(String))
    )

    # Relationships
    organization_rel: Optional[Organization] = Relationship(back_populates="projects")


# -------------------------------------------------------------------------
# Fellowships model
# -------------------------------------------------------------------------
class Fellowship(UUIDBaseTable, table=True):
    __tablename__ = "Fellowships"

    title: Optional[str] = None
    organization: Optional[UUID] = Field(
        default=None, foreign_key="Organizations.id", nullable=True
    )
    hero_image: Optional[str] = None
    location: Optional[str] = None
    location_type: Optional[WorkLocationType] = Field(
        sa_column=Column(SQLEnum(WorkLocationType, name="WORK_LOCATION_TYPE"))
    )
    duration_weeks: Optional[int] = None
    stipend_month: Optional[float] = None
    stipend_currency: Optional[Currency] = Field(
        sa_column=Column(SQLEnum(Currency, name="CURRENCY"))
    )
    application_deadline: Optional[date] = None
    start_date: Optional[date] = None
    description: Optional[str] = None
    featured: Optional[bool] = None
    highlight: Optional[str] = None
    category: Optional[str] = None
    benefits: Optional[List[str]] = Field(
        default_factory=list, sa_column=Column(ARRAY(String))
    )
    requirements: Optional[List[str]] = Field(
        default_factory=list, sa_column=Column(ARRAY(String))
    )
    technologies: Optional[List[str]] = Field(
        default_factory=list, sa_column=Column(ARRAY(String))
    )

    # Relationships
    organization_rel: Optional[Organization] = Relationship(
        back_populates="fellowships"
    )

# -------------------------------------------------------------------------
# User model
# -------------------------------------------------------------------------

class User(UUIDBaseTable, table=True):
    __tablename__ = "Users"

    github_user_name: str = Field(nullable=False, unique=True)
    first_name: str = Field(nullable=False)
    middle_name: Optional[str] = None
    last_name: str = Field(nullable=False)
    rank: Rank = Field(
        default=Rank.UNRANKED,
        sa_column=Column(SQLEnum(Rank, name="RANK"), nullable=False),
    )
    streak: Optional[int] = None