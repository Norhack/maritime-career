from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Integer, Float, Boolean, Index
from backend.database.base import Base


class CompanySignal(Base):
    """Signals that indicate a target company may be hiring."""

    __tablename__ = "company_signals"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), nullable=False, index=True)
    signal_type = Column(String(100), nullable=False, index=True)  # fleet_expansion, office_opening, acquisition, etc.
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    confidence = Column(Float, default=0.0)
    source = Column(String(255))
    published_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_company_signal_company_type", "company_name", "signal_type"),
    )


class TargetCompany(Base):
    """Strategic company watchlist and intelligence record."""

    __tablename__ = "target_companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    sector = Column(String(100), index=True)
    country = Column(String(100), index=True)
    headquarters = Column(String(255))
    website = Column(String(2048))
    priority = Column(String(50), default="medium", index=True)  # low, medium, high
    watchlist_status = Column(String(50), default="active", index=True)
    hiring_probability = Column(Float, default=0.0)
    last_signal_date = Column(DateTime, nullable=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Recruiter(Base):
    """Recruiter or agency contact profile."""

    __tablename__ = "recruiters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=False, index=True)
    role = Column(String(255))
    email = Column(String(255))
    linkedin_url = Column(String(2048))
    phone = Column(String(100))
    active_vacancies = Column(Integer, default=0)
    response_rate = Column(Float, default=0.0)
    last_contact = Column(DateTime, nullable=True)
    notes = Column(Text)
    is_direct = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Application(Base):
    """Application lifecycle and CRM tracking."""

    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, nullable=True, index=True)
    company_name = Column(String(255), nullable=False, index=True)
    position_title = Column(String(255), nullable=False, index=True)
    pipeline_stage = Column(String(50), default="lead", index=True)
    response_rate = Column(Float, default=0.0)
    interview_rate = Column(Float, default=0.0)
    offer_rate = Column(Float, default=0.0)
    time_to_interview = Column(Integer, default=0)
    notes = Column(Text)
    applied_at = Column(DateTime, nullable=True)
    last_follow_up = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MarketInsight(Base):
    """Weekly market intelligence insight."""

    __tablename__ = "market_insights"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    summary = Column(Text, nullable=False)
    category = Column(String(100), index=True)  # hiring, salary, layoffs, fleet, decarbonisation
    confidence = Column(Float, default=0.0)
    published_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SalaryInsight(Base):
    """Estimated compensation range for roles."""

    __tablename__ = "salary_insights"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(255), nullable=False, index=True)
    country = Column(String(100), index=True)
    industry = Column(String(100), index=True)
    seniority = Column(String(100), index=True)
    company = Column(String(255), index=True)
    expected_salary = Column(String(255))
    likely_range = Column(String(255))
    negotiation_recommendation = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class NetworkingReminder(Base):
    """Reminder for recruiter or networking follow-up."""

    __tablename__ = "networking_reminders"

    id = Column(Integer, primary_key=True, index=True)
    contact_type = Column(String(100), index=True)  # recruiter, hiring_manager, colleague, connection
    contact_name = Column(String(255), nullable=False, index=True)
    message = Column(Text, nullable=False)
    due_date = Column(DateTime, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CoachInsight(Base):
    """Weekly AI coach recommendation."""

    __tablename__ = "coach_insights"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100), index=True)  # cv, cover_letter, interview
    title = Column(String(255), nullable=False)
    summary = Column(Text, nullable=False)
    recommendation = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
