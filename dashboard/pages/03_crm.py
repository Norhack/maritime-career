import streamlit as st
from backend.database.connection import SessionLocal
from backend.models.intelligence import Recruiter, Application

st.set_page_config(page_title="CRM", layout="wide")
st.title("Recruiter & Application CRM")

with SessionLocal() as db:
    st.subheader("Recruiters")
    recruiters = db.query(Recruiter).all()
    if recruiters:
        st.dataframe([
            {
                "Name": r.name,
                "Company": r.company,
                "Role": r.role,
                "Active Vacancies": r.active_vacancies,
                "Response Rate": f"{r.response_rate:.0%}" if r.response_rate else "0%",
                "Last Contact": r.last_contact.strftime("%Y-%m-%d") if r.last_contact else "N/A",
                "Notes": r.notes,
            }
            for r in recruiters
        ], use_container_width=True)
    else:
        st.info("No recruiters recorded yet.")

    st.subheader("Applications")
    applications = db.query(Application).all()
    if applications:
        st.dataframe([
            {
                "Company": a.company_name,
                "Position": a.position_title,
                "Stage": a.pipeline_stage,
                "Response Rate": f"{a.response_rate:.0%}" if a.response_rate else "0%",
                "Interview Rate": f"{a.interview_rate:.0%}" if a.interview_rate else "0%",
                "Offer Rate": f"{a.offer_rate:.0%}" if a.offer_rate else "0%",
                "Time to Interview": a.time_to_interview,
                "Notes": a.notes,
            }
            for a in applications
        ], use_container_width=True)
    else:
        st.info("No applications recorded yet.")
