from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.models.intelligence import (
    TargetCompany,
    Recruiter,
    Application,
    MarketInsight,
    SalaryInsight,
    NetworkingReminder,
    CoachInsight,
)

router = APIRouter(prefix="/api/v1", tags=["milestone-4"])


@router.get("/companies")
def list_companies(db: Session = Depends(get_db)):
    companies = db.query(TargetCompany).all()
    return {"companies": [
        {
            "id": c.id,
            "name": c.name,
            "sector": c.sector,
            "country": c.country,
            "priority": c.priority,
            "hiring_probability": c.hiring_probability,
            "watchlist_status": c.watchlist_status,
            "notes": c.notes,
        }
        for c in companies
    ]}


@router.get("/recruiters")
def list_recruiters(db: Session = Depends(get_db)):
    recruiters = db.query(Recruiter).all()
    return {"recruiters": [
        {
            "id": r.id,
            "name": r.name,
            "company": r.company,
            "role": r.role,
            "active_vacancies": r.active_vacancies,
            "response_rate": r.response_rate,
            "last_contact": r.last_contact.isoformat() if r.last_contact else None,
            "notes": r.notes,
            "is_direct": r.is_direct,
        }
        for r in recruiters
    ]}


@router.get("/applications")
def list_applications(db: Session = Depends(get_db)):
    applications = db.query(Application).all()
    return {"applications": [
        {
            "id": a.id,
            "company_name": a.company_name,
            "position_title": a.position_title,
            "pipeline_stage": a.pipeline_stage,
            "response_rate": a.response_rate,
            "interview_rate": a.interview_rate,
            "offer_rate": a.offer_rate,
            "time_to_interview": a.time_to_interview,
            "notes": a.notes,
            "applied_at": a.applied_at.isoformat() if a.applied_at else None,
        }
        for a in applications
    ]}


@router.get("/market-insights")
def list_market_insights(db: Session = Depends(get_db)):
    insights = db.query(MarketInsight).all()
    return {"insights": [
        {
            "id": i.id,
            "title": i.title,
            "summary": i.summary,
            "category": i.category,
            "confidence": i.confidence,
            "published_date": i.published_date.isoformat() if i.published_date else None,
        }
        for i in insights
    ]}


@router.get("/salary-insights")
def list_salary_insights(db: Session = Depends(get_db)):
    insights = db.query(SalaryInsight).all()
    return {"insights": [
        {
            "id": i.id,
            "role": i.role,
            "country": i.country,
            "industry": i.industry,
            "seniority": i.seniority,
            "expected_salary": i.expected_salary,
            "likely_range": i.likely_range,
            "negotiation_recommendation": i.negotiation_recommendation,
        }
        for i in insights
    ]}


@router.get("/networking-reminders")
def list_networking_reminders(db: Session = Depends(get_db)):
    reminders = db.query(NetworkingReminder).all()
    return {"reminders": [
        {
            "id": r.id,
            "contact_type": r.contact_type,
            "contact_name": r.contact_name,
            "message": r.message,
            "due_date": r.due_date.isoformat() if r.due_date else None,
            "completed": r.completed,
        }
        for r in reminders
    ]}


@router.get("/coach-insights")
def list_coach_insights(db: Session = Depends(get_db)):
    insights = db.query(CoachInsight).all()
    return {"insights": [
        {
            "id": i.id,
            "category": i.category,
            "title": i.title,
            "summary": i.summary,
            "recommendation": i.recommendation,
        }
        for i in insights
    ]}
