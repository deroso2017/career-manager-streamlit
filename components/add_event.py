import time
import datetime
import streamlit as st
from dataclasses import asdict
from models.event_model import Event
from storage import load_json, save_json

EVENTS_FILE = "events/events.json"

CATEGORY_COLORS = {
    "Vorstellungsgespräch": "#FF9800",
    "Meeting": "#2196F3",
    "Urlaub": "#4CAF50",
    "Sonstiges": "#9C27B0",
}


def show_event_form():
    is_admin = st.session_state.get("is_admin", False)

    has_end_date = st.checkbox("Enddatum hinzufügen?")

    with st.form("event_form", clear_on_submit=True):
        title = st.text_input("Titel")
        desc = st.text_area("Beschreibung", height=80)

        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Startdatum", datetime.date.today())
        with col2:
            category = st.selectbox("Kategorie", list(CATEGORY_COLORS.keys()))

        end_date = None
        if has_end_date:
            end_date = st.date_input("Enddatum", datetime.date.today())

        col3, col4 = st.columns(2)
        with col3:
            start_time = st.time_input("Startzeit", datetime.time(9, 0))
        with col4:
            end_time = st.time_input("Endzeit", datetime.time(10, 0))

        submitted = st.form_submit_button(
            "💾 Speichern", use_container_width=True, disabled=not is_admin
        )
        if not is_admin:
            st.info("🔒 Nur der Entwickler kann Termine hinzufügen.")
            return

    if submitted:
        if not title:
            st.error("Bitte einen Titel eingeben.")
            return

        event = Event(
            title=title,
            desc=desc,
            date=start_date.isoformat(),
            end_date=end_date.isoformat() if end_date else None,
            time=start_time.strftime("%H:%M"),
            end_time=end_time.strftime("%H:%M"),
            category=category,
            color=CATEGORY_COLORS[category],
        )

        data = load_json(EVENTS_FILE)
        data.append(asdict(event))
        save_json(EVENTS_FILE, data)

        st.success(f"Termin **{title}** gespeichert!")
        time.sleep(1)
        st.rerun()
