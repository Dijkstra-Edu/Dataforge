from typing import List, Optional
from datetime import date, datetime, timezone

from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import ARRAY, Column, Enum as SQLEnum, String, Integer, BigInteger, Float
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from Schema.SQL.Enums.enums import (
    Difficulty, ProjectLevel, Rank, Tools, WorkLocationType,
    EmploymentType, Currency, Cause, CertificationType, Domain,
    LeetcodeTagCategory, Status, TestScoreType
)

# Base class with UUID PK and timestamps
class UUIDBaseTable(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": datetime.now(timezone.utc)}
    )

# -------------------------------------------------------------------------
# User model
# -------------------------------------------------------------------------
class User(UUIDBaseTable, table=True):
    __tablename__ = "User"

    github_user_name: str = Field(nullable=False, unique=True)
    first_name: str = Field(nullable=False)
    middle_name: Optional[str] = None
    last_name: str = Field(nullable=False)
    rank: Rank = Field(
        default=Rank.UNRANKED,
        sa_column=Column(SQLEnum(Rank, name="RANK"))
    )
    streak: Optional[int] = None

    # Relationships
    profile: Optional["Profile"] = Relationship(back_populates="user_rel")
    blog_posts: List["Blog"] = Relationship(back_populates="user_rel")
    links: Optional["Links"] = Relationship(back_populates="user_rel")
    created_tasks: List["Task"] = Relationship(back_populates="creator_rel", sa_relationship_kwargs={"foreign_keys": "[Task.creator_id]"})
    assigned_tasks: List["Task"] = Relationship(back_populates="assignee_rel", sa_relationship_kwargs={"foreign_keys": "[Task.assignee_id]"})

# -------------------------------------------------------------------------
# Profile model
# -------------------------------------------------------------------------
class Profile(UUIDBaseTable, table=True):
    __tablename__ = "Profile"

    user_id: UUID = Field(foreign_key="User.id", nullable=False, unique=True)

    # Relationships
    user_rel: User = Relationship(back_populates="profile")
    education: List["Education"] = Relationship(back_populates="profile_rel")
    work_experience: List["WorkExperience"] = Relationship(back_populates="profile_rel")
    certifications: List["Certifications"] = Relationship(back_populates="profile_rel")
    test_scores: List["TestScores"] = Relationship(back_populates="profile_rel")
    volunteering: List["Volunteering"] = Relationship(back_populates="profile_rel")
    publications: List["Publications"] = Relationship(back_populates="profile_rel")
    projects: List["Projects"] = Relationship(back_populates="profile_rel")
    leetcode: Optional["Leetcode"] = Relationship(back_populates="profile_rel")
    resume: Optional["Resume"] = Relationship(back_populates="profile_rel")

# -------------------------------------------------------------------------
# Location model
# -------------------------------------------------------------------------
class Location(UUIDBaseTable, table=True):
    __tablename__ = "Location"

    city: str = Field(nullable=False)
    state: Optional[str] = None
    country: str = Field(nullable=False)
    longitude: Optional[float] = None
    latitude: Optional[float] = None

    # Relationships
    education: List["Education"] = Relationship(back_populates="location_rel")
    work_experience: List["WorkExperience"] = Relationship(back_populates="location_rel")

# -------------------------------------------------------------------------
# Education model
# -------------------------------------------------------------------------
class Education(UUIDBaseTable, table=True):
    __tablename__ = "Education"

    profile_id: UUID = Field(foreign_key="Profile.id", nullable=False)
    school: str = Field(nullable=False)
    school_type: str = Field(nullable=False)  # Should be an enum if defined
    degree: str = Field(nullable=False)
    field: str = Field(nullable=False)
    currently_studying: bool = Field(nullable=False)
    location: UUID = Field(foreign_key="Location.id", nullable=False)
    location_type: WorkLocationType = Field(
        sa_column=Column(SQLEnum(WorkLocationType, name="WORK_LOCATION_TYPE"))
    )
    start_date: date = Field(nullable=False)
    end_date: Optional[date] = None
    description_general: str = Field(nullable=False)
    description_detailed: Optional[str] = None
    description_less: Optional[str] = None
    work_done: Optional[str] = None
    school_score_multiplier: Optional[float] = None
    tools_used: Optional[List[Tools]] = Field(
        sa_column=Column(ARRAY(SQLEnum(Tools, name="TOOLS")))
    )

    # Relationships
    profile_rel: Profile = Relationship(back_populates="education")
    location_rel: Location = Relationship(back_populates="education")

# -------------------------------------------------------------------------
# WorkExperience model
# -------------------------------------------------------------------------
class WorkExperience(UUIDBaseTable, table=True):
    __tablename__ = "WorkExperience"

    profile_id: UUID = Field(foreign_key="Profile.id", nullable=False)
    title: str = Field(nullable=False)
    employment_type: EmploymentType = Field(
        sa_column=Column(SQLEnum(EmploymentType, name="EMPLOYMENT_TYPE"))
    )
    domain: Optional[List[Domain]] = Field(
        sa_column=Column(ARRAY(SQLEnum(Domain, name="DOMAIN")))
    )
    company_name: str = Field(nullable=False)
    currently_working: bool = Field(nullable=False)
    location: UUID = Field(foreign_key="Location.id", nullable=False)
    location_type: WorkLocationType = Field(
        sa_column=Column(SQLEnum(WorkLocationType, name="WORK_LOCATION_TYPE"))
    )
    start_date: date = Field(nullable=False)
    end_date: Optional[date] = None
    description_general: str = Field(nullable=False)
    description_detailed: Optional[str] = None
    description_less: Optional[str] = None
    work_done: List[str] = Field(
        sa_column=Column(ARRAY(String))
    )
    company_score: Optional[float] = None
    time_spent_multiplier: Optional[float] = None
    work_done_multiplier: Optional[float] = None
    tools_used: Optional[List[Tools]] = Field(
        sa_column=Column(ARRAY(SQLEnum(Tools, name="TOOLS")))
    )

    # Relationships
    profile_rel: Profile = Relationship(back_populates="work_experience")
    location_rel: Location = Relationship(back_populates="work_experience")

# -------------------------------------------------------------------------
# Certifications model
# -------------------------------------------------------------------------
class Certifications(UUIDBaseTable, table=True):
    __tablename__ = "Certifications"

    profile_id: UUID = Field(foreign_key="Profile.id", nullable=False)
    name: str = Field(nullable=False)
    type: CertificationType = Field(
        sa_column=Column(SQLEnum(CertificationType, name="CERTIFICATION_TYPE"))
    )
    issuing_organization: str = Field(nullable=False)
    issue_date: date = Field(nullable=False)
    expiry_date: Optional[date] = None
    credential_id: str = Field(nullable=False)
    credential_url: str = Field(nullable=False)
    tools: Optional[List[Tools]] = Field(
        sa_column=Column(ARRAY(SQLEnum(Tools, name="TOOLS")))
    )

    # Relationships
    profile_rel: Profile = Relationship(back_populates="certifications")

# -------------------------------------------------------------------------
# TestScores model (updated to use UUID and TestScoreType enum)
# -------------------------------------------------------------------------
class TestScores(UUIDBaseTable, table=True):
    __tablename__ = "TestScores"

    profile_id: UUID = Field(foreign_key="Profile.id", nullable=False)
    title: str = Field(nullable=False)
    type: TestScoreType = Field(
        sa_column=Column(SQLEnum(TestScoreType, name="TEST_SCORE_TYPE"))
    )
    score: str = Field(nullable=False)
    test_date: date = Field(nullable=False)
    description: Optional[str] = None

    # Relationships
    profile_rel: Profile = Relationship(back_populates="test_scores")

# -------------------------------------------------------------------------
# Volunteering model (updated to use UUID and currently_volunteering field)
# -------------------------------------------------------------------------
class Volunteering(UUIDBaseTable, table=True):
    __tablename__ = "Volunteering"

    profile_id: UUID = Field(foreign_key="Profile.id", nullable=False)
    organization: str = Field(nullable=False)
    role: str = Field(nullable=False)
    cause: Cause = Field(
        sa_column=Column(SQLEnum(Cause, name="CAUSE"))
    )
    start_date: date = Field(nullable=False)
    end_date: Optional[date] = None
    currently_volunteering: bool = Field(nullable=False)
    description: Optional[str] = None
    tools: Optional[List[Tools]] = Field(
        sa_column=Column(ARRAY(SQLEnum(Tools, name="TOOLS")))
    )

    # Relationships
    profile_rel: Profile = Relationship(back_populates="volunteering")

# -------------------------------------------------------------------------
# Publications model (updated to use UUID)
# -------------------------------------------------------------------------
class Publications(UUIDBaseTable, table=True):
    __tablename__ = "Publications"

    profile_id: UUID = Field(foreign_key="Profile.id", nullable=False)
    title: str = Field(nullable=False)
    publisher: str = Field(nullable=False)
    authors: List[str] = Field(
        sa_column=Column(ARRAY(String), nullable=False)
    )
    publication_date: date = Field(nullable=False)
    publication_url: str = Field(nullable=False)
    description: str = Field(nullable=False)
    tools: Optional[List[Tools]] = Field(
        sa_column=Column(ARRAY(SQLEnum(Tools, name="TOOLS")))
    )

    # Relationships
    profile_rel: Profile = Relationship(back_populates="publications")

# -------------------------------------------------------------------------
# Projects model
# -------------------------------------------------------------------------
class Projects(UUIDBaseTable, table=True):
    __tablename__ = "Projects"

    profile_id: UUID = Field(foreign_key="Profile.id", nullable=False)
    name: str = Field(nullable=False)
    organization: Optional[str] = None
    owner: str = Field(foreign_key="Github.user_name", nullable=False)
    private: bool = Field(nullable=False)
    github_stars: int = Field(nullable=False)
    github_about: Optional[str] = None
    github_open_issues: int = Field(nullable=False)
    github_forks: int = Field(nullable=False)
    description: str = Field(nullable=False)
    domain: Domain = Field(
        sa_column=Column(SQLEnum(Domain, name="DOMAIN"))
    )
    topics: Optional[List[str]] = Field(
        sa_column=Column(ARRAY(String))
    )
    tools: List[Tools] = Field(
        sa_column=Column(ARRAY(SQLEnum(Tools, name="TOOLS")), nullable=False)
    )
    readme: bool = Field(nullable=False)
    licence: bool = Field(nullable=False)
    landing_page: bool = Field(nullable=False)
    landing_page_link: Optional[str] = None
    docs_page: bool = Field(nullable=False)
    docs_page_link: Optional[str] = None
    own_domain_name: bool = Field(nullable=False)
    domain_name: Optional[str] = None
    total_lines_contributed: Optional[int] = None
    improper_uploads: Optional[bool] = None
    complexity_rating: Optional[float] = None
    testing_framework_present: bool = Field(nullable=False)
    testing_framework: Optional[str] = None

    # Relationships
    profile_rel: Profile = Relationship(back_populates="projects")
    owner_rel: "Github" = Relationship(back_populates="projects")

# -------------------------------------------------------------------------
# Leetcode model
# -------------------------------------------------------------------------
class Leetcode(UUIDBaseTable, table=True):
    __tablename__ = "Leetcode"

    profile_id: UUID = Field(foreign_key="Profile.id", nullable=False)
    lc_username: Optional[str] = None
    real_name: Optional[str] = None
    about_me: Optional[str] = None
    school: Optional[str] = None
    websites: Optional[str] = None
    country: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    skill_tags: Optional[List[str]] = Field(
        sa_column=Column(ARRAY(String))
    )
    ranking: Optional[int] = None
    avatar: Optional[str] = None
    reputation: Optional[int] = None
    solution_count: Optional[int] = None
    total_problems_solved: Optional[int] = None
    easy_problems_solved: Optional[int] = None
    medium_problems_solved: Optional[int] = None
    hard_problems_solved: Optional[int] = None
    language_problem_count: Optional[List[str]] = Field(
        sa_column=Column(ARRAY(String))
    )
    attended_contests: Optional[int] = None
    competition_rating: Optional[float] = None
    global_ranking: Optional[int] = None
    total_participants: Optional[int] = None
    top_percentage: Optional[float] = None
    competition_badge: Optional[str] = None

    # Relationships
    profile_rel: Profile = Relationship(back_populates="leetcode")
    badges: List["LeetcodeBadges"] = Relationship(back_populates="leetcode_rel")
    tags: List["LeetcodeTags"] = Relationship(back_populates="leetcode_rel")

# -------------------------------------------------------------------------
# LeetcodeBadges model
# -------------------------------------------------------------------------
class LeetcodeBadges(UUIDBaseTable, table=True):
    __tablename__ = "LeetcodeBadges"

    leetcode_id: UUID = Field(foreign_key="Leetcode.id", nullable=False)
    name: Optional[str] = None
    icon: Optional[str] = None
    hover_text: Optional[str] = None

    # Relationships
    leetcode_rel: Leetcode = Relationship(back_populates="badges")

# -------------------------------------------------------------------------
# LeetcodeTags model
# -------------------------------------------------------------------------
class LeetcodeTags(UUIDBaseTable, table=True):
    __tablename__ = "LeetcodeTags"

    leetcode_id: UUID = Field(foreign_key="Leetcode.id", nullable=False)
    tag_category: Optional[LeetcodeTagCategory] = Field(
        sa_column=Column(SQLEnum(LeetcodeTagCategory, name="LEETCODE_TAG_CATEGORY"))
    )
    tag_name: Optional[str] = None
    problems_solved: Optional[int] = None

    # Relationships
    leetcode_rel: Leetcode = Relationship(back_populates="tags")

# -------------------------------------------------------------------------
# Github model
# -------------------------------------------------------------------------
class Github(UUIDBaseTable, table=True):
    __tablename__ = "Github"

    user_name: str = Field(nullable=False, unique=True)
    github_bio: Optional[str] = None
    followers: Optional[int] = None
    following: Optional[int] = None
    repositories: Optional[int] = None
    current_work: Optional[str] = None
    current_location: Optional[str] = None
    current_timezone: Optional[str] = None
    avatar: Optional[str] = None
    websites: Optional[List[str]] = Field(
        sa_column=Column(ARRAY(String))
    )
    organization: Optional[List[str]] = Field(
        sa_column=Column(ARRAY(String))
    )
    total_lines_contributed: Optional[int] = None
    total_prs_raised: Optional[int] = None
    total_issues_created: Optional[int] = None
    total_repos: Optional[int] = None
    total_commits: Optional[int] = None
    contribution_graph_link: Optional[str] = None

    # Relationships
    projects: List["Projects"] = Relationship(back_populates="owner_rel")

# -------------------------------------------------------------------------
# Links model
# -------------------------------------------------------------------------
class Links(UUIDBaseTable, table=True):
    __tablename__ = "Links"

    user_id: UUID = Field(foreign_key="User.id", nullable=False)
    portfolio_link: Optional[str] = None
    github_user_name: str = Field(nullable=False, unique=True)
    github_link: str = Field(nullable=False)
    linkedin_user_name: str = Field(nullable=False, unique=True)
    linkedin_link: str = Field(nullable=False)
    leetcode_user_name: str = Field(nullable=False, unique=True)
    leetcode_link: str = Field(nullable=False)
    orcid_id: str = Field(nullable=False, unique=True)
    orcid_link: str = Field(nullable=False)

    # Relationships
    user_rel: User = Relationship(back_populates="links")

# -------------------------------------------------------------------------
# Blog model
# -------------------------------------------------------------------------
class Blog(UUIDBaseTable, table=True):
    __tablename__ = "Blog"

    user_id: UUID = Field(foreign_key="User.id", nullable=False)
    title: str = Field(nullable=False)
    description: str = Field(nullable=False)
    publish_date: date = Field(nullable=False)
    tags: List[str] = Field(
        sa_column=Column(ARRAY(String), nullable=False)
    )
    image: str = Field(nullable=False)
    authors: List[str] = Field(
        sa_column=Column(ARRAY(String), nullable=False)
    )
    content: str = Field(nullable=False)

    # Relationships
    user_rel: User = Relationship(back_populates="blog_posts")

# -------------------------------------------------------------------------
# Resume model (updated to make profile_id optional)
# -------------------------------------------------------------------------
class Resume(UUIDBaseTable, table=True):
    __tablename__ = "Resume"

    profile_id: Optional[UUID] = Field(foreign_key="Profile.id", nullable=True)

    # Relationships
    profile_rel: Optional[Profile] = Relationship(back_populates="resume")

# -------------------------------------------------------------------------
# ProjectTask model
# -------------------------------------------------------------------------
class ProjectTask(UUIDBaseTable, table=True):
    __tablename__ = "ProjectTask"

    title: str = Field(nullable=False)
    description: Optional[str] = None
    organization_id: UUID = Field(foreign_key="Organizations.id", nullable=False)

    # Relationships
    tasks: List["Task"] = Relationship(back_populates="project_rel")
    organization_rel: "Organization" = Relationship(back_populates="project_tasks")

# -------------------------------------------------------------------------
# Task model
# -------------------------------------------------------------------------
class Task(UUIDBaseTable, table=True):
    __tablename__ = "Task"

    project_id: UUID = Field(foreign_key="ProjectTask.id", nullable=False)
    title: str = Field(nullable=False)
    description: Optional[str] = None
    status: Status = Field(
        sa_column=Column(SQLEnum(Status, name="STATUS"))
    )
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    labels: Optional[List[str]] = Field(
        sa_column=Column(ARRAY(String))
    )
    issue_url: Optional[str] = None
    creator_id: UUID = Field(foreign_key="User.id", nullable=False)
    reviewer_id: Optional[List[UUID]] = Field(
        sa_column=Column(ARRAY(PG_UUID))
    )
    assignee_id: Optional[UUID] = Field(foreign_key="User.id", nullable=True)
    repository_url: str = Field(nullable=False)

    # Relationships
    project_rel: ProjectTask = Relationship(back_populates="tasks")
    creator_rel: User = Relationship(back_populates="created_tasks", sa_relationship_kwargs={"foreign_keys": "[Task.creator_id]"})
    assignee_rel: Optional[User] = Relationship(back_populates="assigned_tasks", sa_relationship_kwargs={"foreign_keys": "[Task.assignee_id]"})

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
    project_tasks: List["ProjectTask"] = Relationship(back_populates="organization_rel")

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

    technologies: Optional[List[str]] = Field(
        default_factory=list, sa_column=Column(ARRAY(SQLEnum(Tools, name="TOOLS")))
    )

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
    organization: UUID = Field(
        foreign_key="Organizations.id", nullable=False
    )
    organization_logo: Optional[str] = None
    hero_image: Optional[str] = None
    repository: Optional[str] = None

    # languages & frameworks (USER-DEFINED in schema, but let's treat as TEXT ARRAY for flexibility)
    languages: Optional[List[Tools]] = Field(
        sa_column=Column(ARRAY(SQLEnum(Tools, name="TOOLS")))
    )
    frameworks: Optional[List[Tools]] = Field(
        sa_column=Column(ARRAY(SQLEnum(Tools, name="TOOLS")))
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
        default_factory=list, sa_column=Column(ARRAY(SQLEnum(Tools, name="TOOLS")))
    )

    # Relationships
    organization_rel: Optional[Organization] = Relationship(
        back_populates="fellowships"
    )