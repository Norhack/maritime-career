from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.models.intelligence import TargetCompany, MarketInsight, Recruiter, SalaryInsight, NetworkingReminder, CoachInsight

router = APIRouter(prefix="/api/v1", tags=["briefings"])


@router.get("/briefing")
def get_briefing(db: Session = Depends(get_db)):
    companies = db.query(TargetCompany).order_by(TargetCompany.hiring_probability.desc()).limit(3).all()
    insights = db.query(MarketInsight).order_by(MarketInsight.published_date.desc()).limit(3).all()
    recruiters = db.query(Recruiter).order_by(Recruiter.active_vacancies.desc()).limit(3).all()
    salary = db.query(SalaryInsight).first()
    reminders = db.query(NetworkingReminder).filter(NetworkingReminder.completed == False).limit(3).all()
    coach = db.query(CoachInsight).order_by(CoachInsight.created_at.desc()).first()

    return {
        "greeting": "Good morning Sven.",
        "new_opportunities": len(companies),
        "highest_match": {
            "company": companies[0].name if companies else None,
            "role": "Technical Superintendent",
            "match_score": 96 if companies else None,
        },
        "company_news": [
            {"title": i.title, "summary": i.summary} for i in insights
        ],
        "market": {
            "summary": insights[0].summary if insights else "No market data available.",
        },
        "recommendations": [
            {"company": c.name, "reason": c.notes} for c in companies
        ],
        "salary": {
            "role": salary.role if salary else None,
            "expected_salary": salary.expected_salary if salary else None,
            "likely_range": salary.likely_range if salary else None,
        },
        "reminders": [
            {"contact": r.contact_name, "message": r.message} for r in reminders
        ],
        "coach": {
            "title": coach.title if coach else None,
            "summary": coach.summary if coach else None,
        },
    }
