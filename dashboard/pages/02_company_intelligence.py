import streamlit as st
from backend.database.connection import SessionLocal
from backend.models.intelligence import TargetCompany, CompanySignal

st.set_page_config(page_title="Company Intelligence", layout="wide")
st.title("Company Intelligence")

with SessionLocal() as db:
    companies = db.query(TargetCompany).all()
    if not companies:
        st.info("No target companies yet.")
        st.stop()

    for company in companies:
        with st.expander(f"{company.name} — {company.priority} priority"):
            st.write(f"Sector: {company.sector or 'N/A'}")
            st.write(f"Country: {company.country or 'N/A'}")
            st.write(f"Hiring Probability: {company.hiring_probability:.0%}" if company.hiring_probability else "0%")
            st.write(f"Notes: {company.notes or 'No notes.'}")
            signals = db.query(CompanySignal).filter(CompanySignal.company_name == company.name).all()
            if signals:
                st.write("Signals:")
                for signal in signals:
                    st.write(f"- {signal.signal_type}: {signal.title} ({signal.confidence:.0%})")
            else:
                st.write("No signals recorded yet.")
