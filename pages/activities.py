import streamlit as st
from components.add_activity import show_activity_form
from auth import require_login
from storage import load_json

require_login()

st.set_page_config(page_title="Aktivitäten", page_icon=":material/waving_hand:")

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

col1, buff, col2 = st.columns([0.4, 0.6, 0.07])
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

activities = load_json("activities/activity.json")

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
            st.markdown(
                f"""
                {start_str}  
                {end_str}  
                <br>
                {desc}
                """,
                unsafe_allow_html=True,
            )
