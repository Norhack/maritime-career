import streamlit as st
from backend.database.connection import SessionLocal
from backend.models.intelligence import TargetCompany, Recruiter, Application, MarketInsight, SalaryInsight, NetworkingReminder, CoachInsight

st.set_page_config(page_title="Career Intelligence Dashboard", layout="wide")

st.title("Career Intelligence Dashboard")
st.subheader("Executive overview")

with SessionLocal() as db:
    company_count = db.query(TargetCompany).count()
    recruiter_count = db.query(Recruiter).count()
    application_count = db.query(Application).count()
    insight_count = db.query(MarketInsight).count()
    reminder_count = db.query(NetworkingReminder).filter(NetworkingReminder.completed == False).count()

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Target Companies", company_count)
    col2.metric("Recruiters", recruiter_count)
    col3.metric("Applications", application_count)
    col4.metric("Market Insights", insight_count)
    col5.metric("Open Reminders", reminder_count)

    st.markdown("### Recent activity")
    st.dataframe(
        [
            {
                "Type": "Company",
                "Name": c.name,
                "Priority": c.priority,
                "Hiring Probability": f"{c.hiring_probability:.0%}" if c.hiring_probability else "0%",
            }
            for c in db.query(TargetCompany).order_by(TargetCompany.created_at.desc()).limit(10)
        ],
        use_container_width=True,
    )
