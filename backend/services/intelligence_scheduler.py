from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from backend.database.connection import SessionLocal
from backend.models.intelligence import (
    TargetCompany,
    CompanySignal,
    Recruiter,
    Application,
    MarketInsight,
    SalaryInsight,
    NetworkingReminder,
    CoachInsight,
)


class IntelligenceScheduler:
    """Background scheduler for daily and weekly intelligence jobs."""

    def __init__(self):
        self.scheduler = BackgroundScheduler()

    def start(self):
        self.scheduler.add_job(self.run_daily_briefing, "interval", hours=24, id="daily_briefing")
        self.scheduler.add_job(self.run_weekly_report, "interval", weeks=1, id="weekly_report")
        self.scheduler.start()

    def stop(self):
        self.scheduler.shutdown(wait=False)

    def run_daily_briefing(self):
        with SessionLocal() as db:
            # Seed sample data if empty to demonstrate the briefing flow.
            if db.query(TargetCompany).count() == 0:
                db.add_all([
                    TargetCompany(
                        name="DNV",
                        sector="Energy",
                        country="Norway",
                        priority="high",
                        hiring_probability=0.95,
                        notes="High recruiting signal for technical and commercial roles.",
                    ),
                    TargetCompany(
                        name="Wärtsilä",
                        sector="Energy",
                        country="Finland",
                        priority="high",
                        hiring_probability=0.9,
                        notes="Expanding marine and energy services.",
                    ),
                    TargetCompany(
                        name="Wilhelmsen",
                        sector="Shipping",
                        country="Norway",
                        priority="high",
                        hiring_probability=0.88,
                        notes="Fleet and logistics expansion signals.",
                    ),
                ])
                db.commit()

            if db.query(MarketInsight).count() == 0:
                db.add(MarketInsight(
                    title="Norway hiring increased 14%",
                    summary="Regional hiring activity in Norway is up across shipping and offshore services.",
                    category="hiring",
                    confidence=0.84,
                ))
                db.commit()

            if db.query(SalaryInsight).count() == 0:
                db.add(SalaryInsight(
                    role="Technical Superintendent",
                    country="Norway",
                    industry="Shipping",
                    seniority="Senior",
                    expected_salary="NOK 1,200,000",
                    likely_range="NOK 1,050,000 - 1,400,000",
                    negotiation_recommendation="Position around the midpoint and highlight fleet leadership experience.",
                ))
                db.commit()

            if db.query(Recruiter).count() == 0:
                db.add(Recruiter(
                    name="Lars Hansen",
                    company="Faststream",
                    role="Senior Consultant",
                    active_vacancies=4,
                    response_rate=0.78,
                    notes="High signal for commercial and technical leadership roles.",
                    is_direct=False,
                ))
                db.commit()

            if db.query(NetworkingReminder).count() == 0:
                db.add(NetworkingReminder(
                    contact_type="recruiter",
                    contact_name="Lars Hansen",
                    message="Follow up with Lars about upcoming technical superintendent vacancies.",
                    due_date=datetime.utcnow(),
                ))
                db.commit()

            if db.query(CoachInsight).count() == 0:
                db.add(CoachInsight(
                    category="cv",
                    title="Strengthen maritime keywords",
                    summary="Your CV is strong, but it should emphasize leadership and fleet operations keywords.",
                    recommendation="Add vessel operations, maintenance strategy, and commercial leadership keywords.",
                ))
                db.commit()

            print("[daily briefing] intelligence snapshot updated")

    def run_weekly_report(self):
        with SessionLocal() as db:
            if db.query(MarketInsight).count() < 3:
                db.add_all([
                    MarketInsight(
                        title="Offshore activity increasing in North Sea",
                        summary="Offshore operators are expanding engineering and commercial capacity.",
                        category="fleet",
                        confidence=0.8,
                    ),
                    MarketInsight(
                        title="Decarbonisation projects driving hiring",
                        summary="Vessel retrofit and sustainability projects are increasing hiring demand.",
                        category="decarbonisation",
                        confidence=0.79,
                    ),
                ])
                db.commit()

            print("[weekly report] market intelligence refreshed")
