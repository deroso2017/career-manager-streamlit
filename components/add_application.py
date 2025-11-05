import streamlit as st
import time
import datetime
import json
from dataclasses import asdict
from pathlib import Path
from models.application_model import Application


# ---------- Configuration ----------
UPLOAD_FOLDER = Path("files")
UPLOAD_FOLDER.mkdir(exist_ok=True)
JSON_FILE = UPLOAD_FOLDER / "applications.json"


# ---------- Form Renderer ----------
def show_application_form():
    """Render the Streamlit job application form and handle saving."""

    with st.form("application_form", clear_on_submit=True):
        company = st.text_input("Firma")
        date = st.date_input("Datum", datetime.date.today())
        status = st.selectbox("Status", ["Übermittelt", "Abgesagt"], index=0)
        platform = st.selectbox("Platform", ["LinkedIn", "Arbeitsagentur", "Join", "Instaffo", "Stepstone", "Initiative"], index=1)
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
    unsafe_allow_html=True
    )  
        

    if submitted:
        if not company or not uploaded_file:
            st.error("Bitte Firma eingeben und eine PDF-Datei hochladen.")
            return

        # Save the uploaded PDF file
        save_path = UPLOAD_FOLDER / uploaded_file.name
        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())

        # Create Application object
        app_entry = Application(
            company=company,
            date=date.isoformat(),
            status=status,
            platform=platform,
            link=str(save_path)
        )

        # Read or initialize JSON data
        data = []
        if JSON_FILE.exists():
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []

        # Update existing entry if same company exists
        updated = False
        for i, existing in enumerate(data):
            if existing["company"].lower() == company.lower():
                data[i] = asdict(app_entry)
                updated = True
                break

        if not updated:
            data.append(asdict(app_entry))

        # Save to JSON
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        st.success(f"Bewerbung für **{company}** wurde gespeichert!")
        time.sleep(1)
        st.rerun()


