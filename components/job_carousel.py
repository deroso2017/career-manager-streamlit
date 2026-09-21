import urllib.parse
import requests
import streamlit as st

API_URL = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v6/jobs"
API_KEY = "jobboerse-jobsuche"


@st.cache_data(ttl=600)
def fetch_jobs(keyword: str, location: str = "Deutschland", size: int = 15):
    """Fetch job offers from Bundesagentur für Arbeit API."""
    params = {"was": keyword, "size": size, "page": 1}
    if location and location.strip() and location.lower() != "deutschland":
        params["wo"] = location

    headers = {"X-API-Key": API_KEY, "User-Agent": "Mozilla/5.0"}

    try:
        resp = requests.get(API_URL, params=params, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        # --- DEBUGGING: Zeige die rohe API-Antwort in Streamlit an ---
        # st.write("Rohe API-Antwort von v6:", data)
        # -----------------------------------------------------------

        offers = data.get("stellenangebote", [])
        if not offers:
            for key, value in data.items():
                if isinstance(value, list):
                    offers = value
                    break

        if isinstance(offers, dict):
            offers = [offers]

        jobs = []
        for o in offers:
            # In der fetch_jobs Funktion innerhalb der for o in offers Schleife:
            location_name = "—"

            # Die API der Arbeitsagentur nutzt 'stellenlokationen'
            lokationen = o.get("stellenlokationen")
            if isinstance(lokationen, list) and len(lokationen) > 0:
                # Wir nehmen standardmäßig den ersten Standort
                first_loc = lokationen[0]
                if isinstance(first_loc, dict):
                    adresse = first_loc.get("adresse")
                    if isinstance(adresse, dict):
                        plz = str(adresse.get("plz", ""))
                        ort = adresse.get("ort", "")
                        parts = [p for p in [plz, ort] if p]
                        if parts:
                            location_name = " ".join(parts)
                        else:
                            location_name = (
                                adresse.get("region") or adresse.get("land") or "—"
                            )

            # Falls wider Erwarten doch ein einzelnes 'arbeitsort'-Feld existiert
            if location_name == "—":
                arbeitsort = o.get("arbeitsort")
                if isinstance(arbeitsort, dict):
                    plz = str(arbeitsort.get("plz", ""))
                    ort = arbeitsort.get("ort", "")
                    parts = [p for p in [plz, ort] if p]
                    if parts:
                        location_name = " ".join(parts)
                elif isinstance(arbeitsort, str) and arbeitsort.strip():
                    location_name = arbeitsort

            # Append simplified job dict
            jobs.append(
                {
                    "title": o.get(
                        "stellenangebotsTitel",
                        o.get("titel", o.get("bezeichnung", "—")),
                    ),
                    "company": o.get("firma", o.get("arbeitgeber", "—")),
                    "location": location_name,
                    "reference_nr": o.get("referenznummer", o.get("refnr")) or "#",
                    "entry_date": o.get("eintrittszeitraum", {}).get("von")
                    or o.get("eintrittsdatum")
                    or "#",
                    "public_date": o.get("veroeffentlichungszeitraum", {}).get("von")
                    or o.get(
                        "aktuelleVeroeffentlichungsdatum",
                        o.get("veroeffentlichungsdatum"),
                    )
                    or "#",
                }
            )
        return jobs

    except Exception as e:
        st.error(f"Fehler beim Abrufen der Daten: {e}")
        return []


def job_carousel(
    keyword: str = "Webentwickler", location: str = "Deutschland", size: int = 30
):
    """Display job cards in groups of 3 with navigation buttons and equal height."""
    st.subheader(f"💼 Aktuelle Jobs: {keyword} in {location}")

    jobs = fetch_jobs(keyword, location, size=size)

    if not jobs:
        st.warning("Keine passenden Stellenangebote gefunden.")
        st.session_state.carousel_index = 0
        return

    # Pagination index speichern
    if "carousel_index" not in st.session_state:
        st.session_state.carousel_index = 0

    st.markdown(
        """
        <style>
        .job-card {
            background: linear-gradient(135deg, #262730, #0E1117);
            padding: 1.5rem 1rem;
            border-radius: 1rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.35);
            transition: transform 0.25s ease, box-shadow 0.25s ease;
            color: #f5f5f5;
            height: 300px;
            display: flex;
            flex-direction: column;
            width: 100%; 
            position: relative;
        }
        .job-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 18px rgba(0,0,0,0.45);
        }
        .job-title {
            color: #14B8A6 !important;
            font-weight: 700;
            font-size: 1.1rem;
            margin-bottom: 0.3rem;
            text-decoration: none !important;
            display: block;
        }
        .job-title:hover {
            text-decoration: underline !important;
        }
        .company-link {
            color: #fff !important;
            font-weight: 600;
            font-size: 14px;
            text-decoration: none;
            display: inline-block;
        }
        .company-link:hover {
            opacity: 0.8;
            text-decoration: underline;
        }
        .job-meta {
            font-size: 0.9rem;
            color: #bbb;
            margin-top: auto !important;
            line-height: 1.4;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 3 Jobs pro Seite
    start = st.session_state.carousel_index
    end = start + 3
    visible_jobs = jobs[start:end]

    cols = st.columns(3)
    for col, job in zip(cols, visible_jobs):
        url = f"https://www.arbeitsagentur.de/jobsuche/jobdetail/{job['reference_nr']}"
        company_query = urllib.parse.quote(f'"{job["company"]}"')
        google_url = f"https://www.google.com/search?q={company_query}"

        with col:
            st.markdown(
                f"""
                <div class="job-card">
                    <div>
                        <a href="{url}" target="_blank" class="job-title">{job['title']}</a>
                        <a href="{google_url}" target="_blank" class="company-link">{job['company']}</a>
                    </div>
                    <div class="job-meta">
                        <div style="display: flex; margin-bottom: 6px">
                            <div style="margin-right: 4px">📍</div>
                            <div>{job['location']}</div>
                        </div>
                        <div style="display: flex; margin-bottom: 6px">
                            <div style="margin-right: 4px">📅</div>
                            <div>Veröffentlicht: {job['public_date']}</div>
                        </div>
                        <div style="display: flex; margin-bottom: 6px">
                            <div style="margin-right: 4px">🗓</div>
                            <div>Eintritt: {job['entry_date']}</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Navigationsbuttons (zentriert)
    st.markdown("<br>", unsafe_allow_html=True)
    button_cols = st.columns([1.2, 3, 1.2])
    with button_cols[0]:
        if st.button("‹ Vorherige Seite"):
            st.session_state.carousel_index = max(
                0, st.session_state.carousel_index - 3
            )
            st.rerun()
    with button_cols[2]:
        if st.button("Nächste Seite ›"):
            if st.session_state.carousel_index + 3 < len(jobs):
                st.session_state.carousel_index += 3
            st.rerun()
