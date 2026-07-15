import streamlit as st
import time
import datetime
import pandas as pd
from storage import upload_file, load_json, save_json

APPLICATIONS_FILE = "applications/applications.json"


def show_application_form(edit_data=None):
    is_edit = edit_data is not None
    is_admin = st.session_state.get("is_admin", False)

    # Pre-process data for the form
    with st.form("application_form"):
        company = st.text_input(
            "Firma", value=edit_data.get("company", "") if is_edit else ""
        )

        # Handle date parsing
        default_date = (
            pd.to_datetime(edit_data["date"]).date()
            if is_edit
            else datetime.date.today()
        )
        date = st.date_input("Datum", value=default_date)

        status = st.selectbox(
            "Status",
            ["Übermittelt", "Abgesagt"],
            index=(
                ["Übermittelt", "Abgesagt"].index(
                    edit_data.get("status", "Übermittelt")
                )
                if is_edit
                else 0
            ),
        )

        platforms = [
            "LinkedIn",
            "Arbeitsagentur",
            "Join",
            "Instaffo",
            "Stepstone",
            "Initiative",
        ]
        platform = st.selectbox(
            "Platform",
            platforms,
            index=(
                platforms.index(edit_data.get("platform", "LinkedIn")) if is_edit else 0
            ),
        )

        uploaded_file = st.file_uploader(
            "📎 Neue PDF hochladen (optional)", type=["pdf"]
        )

        submitted = st.form_submit_button(
            "💾 Speichern", use_container_width=True, disabled=not is_admin
        )
        if not is_admin:
            st.info(
                "🔒 Nur der Entwickler kann Bewerbungen hinzufügen oder bearbeiten."
            )

    if submitted:
        if not company:
            st.error("Bitte Firma eingeben.")
            return

        # Maintain existing link if no new file is provided
        pdf_path = edit_data.get("link", "") if is_edit else ""
        if uploaded_file:
            pdf_path = f"applications/{uploaded_file.name}"
            upload_file(uploaded_file.getvalue(), pdf_path)

        new_entry = {
            "company": company,
            "date": date.isoformat(),
            "status": status,
            "platform": platform,
            "link": pdf_path,
        }

        data = load_json(APPLICATIONS_FILE)

        if is_edit:
            # Match by original company and date (as they define the record)
            for i, item in enumerate(data):
                if (
                    item["company"] == edit_data["company"]
                    and item["date"] == edit_data["date"]
                ):
                    data[i] = new_entry
                    break
        else:
            data.append(new_entry)

        save_json(APPLICATIONS_FILE, data)
        st.success("Erfolgreich gespeichert!")
        time.sleep(1)  # Optional: brief pause to ensure data is saved before rerun
        st.rerun()
