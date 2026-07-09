import time
import datetime
import json
import streamlit as st
from dataclasses import asdict
from pathlib import Path
from models.activity_model import Activity

# ---------- Configuration ----------
UPLOAD_FOLDER = Path("files")
UPLOAD_FOLDER.mkdir(exist_ok=True)
JSON_FILE = UPLOAD_FOLDER / "activity.json"


# ---------- Form Renderer ----------
def show_activity_form():
    """Render the Streamlit job application form and handle saving."""

    # Checkbox outside form → updates immediately
    has_end_date = st.checkbox("Enddatum hinzufügen?")

    with st.form("application_form", clear_on_submit=True):
        title = st.text_input("Title")
        desc = st.text_area("Beschreibung")
        start_date = st.date_input("Startdatum", datetime.date.today())

        end_date = None
        if has_end_date:
            end_date = st.date_input("Enddatum")

        submitted = st.form_submit_button("💾 Speichern")

    # ---- CSS for full-width submit button ----
    st.markdown(
        """
        <style>
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

    # ---- Handle form submission ----
    if submitted:
        if not title or not desc:
            st.error("Bitte Title und Beschreibung eingeben.")
            return

        activity_entry = Activity(
            title,
            desc,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat() if end_date else None,
        )

        data = []
        if JSON_FILE.exists():
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []

        updated = False
        for i, existing in enumerate(data):
            if existing["title"].lower() == title.lower():
                data[i] = asdict(activity_entry)
                updated = True
                break

        if not updated:
            data.append(asdict(activity_entry))

        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        st.success(f"Neue Aktivität als **{title}** wurde gespeichert!")
        time.sleep(1)
        st.rerun()
