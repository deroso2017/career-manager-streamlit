import time
import datetime
import streamlit as st
from dataclasses import asdict
from models.application_model import Application
from storage import upload_file, load_json, save_json

APPLICATIONS_FILE = "applications/applications.json"


# ---------- Form Renderer ----------
def show_application_form():
    """Render the Streamlit job application form and handle saving."""

    with st.form("application_form", clear_on_submit=True):
        company = st.text_input("Firma")
        date = st.date_input("Datum", datetime.date.today())
        status = st.selectbox("Status", ["Übermittelt", "Abgesagt"], index=0)
        platform = st.selectbox(
            "Platform",
            [
                "LinkedIn",
                "Arbeitsagentur",
                "Join",
                "Instaffo",
                "Stepstone",
                "Initiative",
            ],
            index=1,
        )
        uploaded_file = st.file_uploader("📎 Bewerbungen hochladen (PDF)", type=["pdf"])
        submitted = st.form_submit_button("💾 Speichern")

    st.markdown(
        """
    <style>
    /* Target the specific submit button container by key part */
    .st-key-FormSubmitter-application_form----Speichern {
        width: 100% !important;
    }

    .st-key-FormSubmitter-application_form----Speichern button {
        width: 100%;      
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    if submitted:
        if not company or not uploaded_file:
            st.error("Bitte Firma eingeben und eine PDF-Datei hochladen.")
            return

        pdf_path = f"applications/{uploaded_file.name}"

        upload_file(uploaded_file.getvalue(), pdf_path)

        # Create Application object
        app_entry = Application(
            company=company,
            date=date.isoformat(),
            status=status,
            platform=platform,
            link=pdf_path,
        )

        # Read or initialize JSON data
        data = load_json(APPLICATIONS_FILE)

        # Update existing entry if same company exists
        updated = False
        for i, existing in enumerate(data):
            if existing["company"].lower() == company.lower():
                data[i] = asdict(app_entry)
                updated = True
                break

        if not updated:
            data.append(asdict(app_entry))

        save_json(APPLICATIONS_FILE, data)

        st.success(f"Bewerbung für **{company}** wurde gespeichert!")
        time.sleep(1)
        st.rerun()
