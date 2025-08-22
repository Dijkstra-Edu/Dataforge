from typing import List, Optional
from datetime import datetime, date
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from Entities.SQL.Enums.enums import LocationType, EmploymentType, Currency
from sqlalchemy import ARRAY, Column, Enum as SQLEnum, JSON, String

# Base class with UUID PK and timestamps
class UUIDBaseTable(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

# Organization model
class Organization(UUIDBaseTable, table=True):
    __tablename__ = "Organizations"

    name: Optional[str] = None
    jobs: List["Job"] = Relationship(back_populates="organization_rel")


# Job model
class Job(UUIDBaseTable, table=True):
    __tablename__ = "Jobs"

    title: Optional[str] = None
    department: Optional[str] = None
    company_name: Optional[str] = None
    company_logo: Optional[str] = None
    hero_image: Optional[str] = None
    location: Optional[str] = None
    location_type: Optional[LocationType] = Field(
        sa_column=Column(SQLEnum(LocationType, name="location_type_enum"))
    )
    employment_type: Optional[EmploymentType] = Field(
        sa_column=Column(SQLEnum(EmploymentType, name="employment_type_enum"))
    )
    experience_level: Optional[str] = None
    experience_yoe: Optional[float] = None
    posted_date: Optional[date] = None
    salary_annual_min: Optional[int] = None
    salary_annual_max: Optional[int] = None
    salary_currency: Optional[Currency] = Field(
        sa_column=Column(SQLEnum(Currency, name="currency_enum"))
    )
    description: Optional[str] = None
    featured: Optional[bool] = None
    highlight: Optional[str] = None
    category: Optional[str] = None
    perks: Optional[List[str]] = Field(
        default_factory=list,
        sa_column=Column(ARRAY(String))
    )

    # Foreign key to Organization
    organization: Optional[UUID] = Field(default=None, foreign_key="Organizations.id", nullable=True)
    organization_rel: Optional[Organization] = Relationship(back_populates="jobs")
