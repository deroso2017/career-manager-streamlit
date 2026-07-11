import streamlit as st
import requests
import urllib.parse

API_URL = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs"
API_KEY = "jobboerse-jobsuche"


@st.cache_data(ttl=600)
def fetch_jobs(keyword: str, location: str = "Deutschland", size: int = 15):
    """Fetch job offers from Bundesagentur für Arbeit API."""
    params = {"was": keyword, "size": size, "page": 1}
    if location and location.strip() and location.lower() != "deutschland":
        params["wo"] = location

    headers = {"X-API-Key": API_KEY}

    try:
        resp = requests.get(API_URL, params=params, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        offers = data.get("stellenangebote", [])
        if isinstance(offers, dict):
            offers = [offers]

        jobs = []
        for o in offers:
            # Extract location
            location_raw = o.get("arbeitsort")
            if isinstance(location_raw, dict):
                location_name = (
                    location_raw.get("ort")
                    or location_raw.get("region")
                    or location_raw.get("land")
                )
            else:
                location_name = location_raw

            # Append simplified job dict
            jobs.append(
                {
                    "title": o.get("titel", "—"),
                    "company": o.get("arbeitgeber"),
                    "location": location_name or "—",
                    "reference_nr": o.get("refnr") or "#",
                    "entry_date": o.get("eintrittsdatum") or "#",
                    "public_date": o.get("aktuelleVeroeffentlichungsdatum") or "#",
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
        .job-container {
                width: 100% !important; 
                cursor: pointer;
                display: block;
                position: absolute;
                top: 0; 
                left: 0; 
                height: 100%;
        }
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
            position: absolute; 
            top: 0; 
            left: 0;
        }
        .job-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 18px rgba(0,0,0,0.45);
        }
        .job-title {
            color: #33E6B3 !important;
            font-weight: 700;
            font-size: 1.1rem;
            margin-bottom: 0.3rem;
            text-decoration: none !important;
        }
        .company-link {
        color: #fff !important;
        font-weight: 600;
        font-size: 14px;
        text-decoration: none;
        z-index: 50;
        }

        .company-link:hover {
        opacity: 0.8;
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
                <div style="position: relative; min-height: 300px;">
                    <a
                        class="job-container"
                        href="{url}"
                        target="_blank"
                    >
                        <div class="job-card">
                        <div
                            style="
                            display: flex;
                            flex-direction: column;
                            min-height: 100%;
                            "
                        >
                            <a class="job-title">{job['title']}</a>
                            <a href="{google_url}" target="_blank" class="company-link"
                            >{job['company']}
                            </a>
                            <div class="job-meta">
                            <div style="display: flex; margin-bottom: 8px">
                                <div style="margin-right: 4px">📍</div>
                                <div>{job['location']}</div>
                            </div>
                            <div style="display: flex; margin-right: 4px">
                                <div style="margin-right: 4px">📅</div>
                                <div>Veröffentlichungsdatum: {job['public_date']}</div>
                            </div>
                            <div style="display: flex; margin-bottom: 8px">
                                <div style="margin-right: 4px">🗓</div>
                                <div>Eintrittsdatum: {job['entry_date']}</div>
                            </div>
                            </div>
                        </div>
                        </div>
                    </a>
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
