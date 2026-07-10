import streamlit as st
from auth import require_login

require_login()

from components.job_carousel import job_carousel

st.set_page_config(page_title="Jobbörse", page_icon=":material/dashboard:")
st.title("Jobbörse")

# Main keyword (job title)
keyword = st.selectbox(
    "Berufsbezeichnung / Stichwort",
    [
        "Webentwickler",
        "Frontend Entwickler",
        "Anwendungsentwickler",
        "Software Engineer",
        "Fullstack Entwickler",
    ],
)

# selectbox for technology stack
tech = st.selectbox(
    "Technologie (optional)", ["", "React", "Angular", "Python", "TypeScript"]
)

location = st.text_input("Ort / Region", "Deutschland")

# Combine keyword + tech for search
search_term = f"{keyword} {tech}".strip()

# Show the carousel from the module
job_carousel(search_term, location, size=20)

st.sidebar.write("""
Auf dieser Seite kann ich gezielt nach **aktuellen Jobangeboten** suchen.  
Sie dient als persönliche **Jobbörse**, die auf meine Interessen und mein Technologiestack abgestimmt ist.
                 
**Funktionen:**
- 💼 *Berufsbezeichnung:*  
  Wähle den gewünschten Jobtitel aus, z. B. *Webentwickler* oder *Software Engineer*.
- ⚙️ *Technologie-Filter:* 
  Optional kann ich eine Technologie wie *React*, *Python* oder *TypeScript* hinzufügen, um die Suche zu verfeinern.
- 📍 *Ort / Region:* 
  Gib an, in welchem Land oder welcher Stadt du arbeiten möchtest (Standard: Deutschland).
- 🔎 *Job-Karussell:* 
  Die Ergebnisse werden automatisch im Karussell angezeigt – mit relevanten Jobangeboten aus verschiedenen Quellen.
""")


# url = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs"
# headers = {"X-API-Key": "jobboerse-jobsuche"}
# params = {"was": "Webentwickler", "size": 5}
# r = requests.get(url, headers=headers, params=params)
# print(r.status_code)
# # print(r.json())
# st.write(r.json())
