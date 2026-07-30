import streamlit as st
from backend.database.connection import SessionLocal
from backend.models.intelligence import MarketInsight, SalaryInsight, NetworkingReminder, CoachInsight

st.set_page_config(page_title="Market Intelligence", layout="wide")
st.title("Market Intelligence")

with SessionLocal() as db:
    st.subheader("Market Insights")
    insights = db.query(MarketInsight).order_by(MarketInsight.published_date.desc()).all()
    for insight in insights:
        with st.expander(f"{insight.title} ({insight.category})"):
            st.write(insight.summary)
            st.write(f"Confidence: {insight.confidence:.0%}")

    st.subheader("Salary Insights")
    salary_insights = db.query(SalaryInsight).all()
    if salary_insights:
        st.dataframe([
            {
                "Role": s.role,
                "Country": s.country,
                "Industry": s.industry,
                "Seniority": s.seniority,
                "Expected Salary": s.expected_salary,
                "Likely Range": s.likely_range,
                "Negotiation Recommendation": s.negotiation_recommendation,
            }
            for s in salary_insights
        ], use_container_width=True)

    st.subheader("Networking Reminders")
    reminders = db.query(NetworkingReminder).filter(NetworkingReminder.completed == False).all()
    for reminder in reminders:
        st.write(f"- {reminder.contact_name} ({reminder.contact_type}): {reminder.message}")

    st.subheader("Coach Insights")
    coach_insights = db.query(CoachInsight).all()
    for insight in coach_insights:
        st.write(f"- {insight.title}: {insight.summary}")
