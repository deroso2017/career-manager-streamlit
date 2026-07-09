import json
import streamlit as st
from pathlib import Path
from components.add_activity import show_activity_form
from auth import require_login

require_login()

# ---------- Configuration ----------
UPLOAD_FOLDER = Path("files")
JSON_FILE = UPLOAD_FOLDER / "activity.json"

st.set_page_config(page_title="Aktivitäten", page_icon=":material/waving_hand:")

col1, buff, col2 = st.columns([.4, .6, .07])
with col1:
    st.title("Aktivitäten")
with col2:
    @st.dialog("📂 Aktivität")
    def add():
        show_activity_form()
        
    st.write("")
    st.write("")
    if st.button("**+**"):
        add()

# Load activities from JSON
if not JSON_FILE.exists():
    st.info("Noch keine Aktivitäten gespeichert.")
else:
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        try:
            activities = json.load(f)
        except json.JSONDecodeError:
            st.error("Fehler beim Lesen der Datei.")
            activities = []

    if not activities:
        st.info("Noch keine Aktivitäten gespeichert.")
    else:
        # Loop through and display each activity
        for activity in activities:
            title = activity.get("title", "Ohne Titel")
            desc = activity.get("desc", "")
            start_date = activity.get("start_date", "")
            end_date = activity.get("end_date", None)

            # Format dates
            start_str = f"**Startdatum:** {start_date}"
            end_str = f"**Enddatum:** {end_date}" if end_date else "**Enddatum:** –"

            with st.expander(f"{title}"):
                st.markdown(f"""
                {start_str}  
                {end_str}  
                <br>
                {desc}
                """, unsafe_allow_html=True)

st.sidebar.write("""
Auf dieser Seite kann ich mein **beruflichen Aktivitäten** dokumentieren und verwalten.  
Sie dient als persönliches Logbuch, um den Überblick über Weiterbildungen, Projekte oder Bewerbungsaktivitäten zu behalten.

**Funktionen:**
- ➕ *Aktivität hinzufügen:* 
  Über den Button **„+“** kann ich neue Aktivitäten wie Kurse, Projekte oder Workshops eintragen.
- 📂 *Aktivitätenübersicht:*  
  Alle gespeicherten Aktivitäten werden übersichtlich mit Titel, Beschreibung und Zeitspanne angezeigt.
- 📅 *Datumsverwaltung:* 
  Sowohl Start- als auch Enddatum jeder Aktivität werden dargestellt.
""")
