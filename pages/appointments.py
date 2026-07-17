import calendar
import datetime
import streamlit as st
from components.add_event import show_event_form, CATEGORY_COLORS
from auth import require_login
from storage import load_json

require_login()

st.set_page_config(page_title="Kalender", page_icon=":material/calendar_today:")


# German public holidays per federal state
def get_holidays(year: int, state: str) -> dict[str, str]:
    """Returns {date_iso: holiday_name} for the given year and German state."""
    fixed = {
        f"{year}-01-01": "Neujahr",
        f"{year}-05-01": "Tag der Arbeit",
        f"{year}-10-03": "Tag der Deutschen Einheit",
        f"{year}-12-25": "1. Weihnachtstag",
        f"{year}-12-26": "2. Weihnachtstag",
    }

    # Easter Sunday (Anonymous Gregorian algorithm)
    a, b, c = year % 19, year % 4, year % 7
    d = (19 * a + 24) % 30
    e = (2 * b + 4 * c + 6 * d + 5) % 7
    easter_day = 22 + d + e
    if easter_day > 31:
        easter_day -= 31
        easter = datetime.date(year, 4, easter_day)
    else:
        easter = datetime.date(year, 3, easter_day)
    # Special corrections
    if easter == datetime.date(year, 4, 26):
        easter = datetime.date(year, 4, 19)
    if easter == datetime.date(year, 4, 25) and d == 28 and e == 6 and a > 10:
        easter = datetime.date(year, 4, 18)

    movable = {
        (easter - datetime.timedelta(days=2)).isoformat(): "Karfreitag",
        easter.isoformat(): "Ostersonntag",
        (easter + datetime.timedelta(days=1)).isoformat(): "Ostermontag",
        (easter + datetime.timedelta(days=39)).isoformat(): "Christi Himmelfahrt",
        (easter + datetime.timedelta(days=49)).isoformat(): "Pfingstsonntag",
        (easter + datetime.timedelta(days=50)).isoformat(): "Pfingstmontag",
    }

    state_specific = {
        "Baden-Württemberg": {
            f"{year}-01-06": "Heilige Drei Könige",
            f"{year}-11-01": "Allerheiligen",
            (easter + datetime.timedelta(days=60)).isoformat(): "Fronleichnam",
        },
        "Bayern": {
            f"{year}-01-06": "Heilige Drei Könige",
            f"{year}-08-15": "Mariä Himmelfahrt",
            f"{year}-11-01": "Allerheiligen",
            (easter + datetime.timedelta(days=60)).isoformat(): "Fronleichnam",
        },
        "Berlin": {f"{year}-03-08": "Internationaler Frauentag"},
        "Brandenburg": {
            f"{year}-10-31": "Reformationstag",
            f"{year}-03-08": "Internationaler Frauentag",
        },
        "Bremen": {f"{year}-10-31": "Reformationstag"},
        "Hamburg": {f"{year}-10-31": "Reformationstag"},
        "Hessen": {
            (easter + datetime.timedelta(days=60)).isoformat(): "Fronleichnam",
        },
        "Mecklenburg-Vorpommern": {f"{year}-10-31": "Reformationstag"},
        "Niedersachsen": {f"{year}-10-31": "Reformationstag"},
        "Nordrhein-Westfalen": {
            f"{year}-11-01": "Allerheiligen",
            (easter + datetime.timedelta(days=60)).isoformat(): "Fronleichnam",
        },
        "Rheinland-Pfalz": {
            f"{year}-11-01": "Allerheiligen",
            (easter + datetime.timedelta(days=60)).isoformat(): "Fronleichnam",
        },
        "Saarland": {
            f"{year}-08-15": "Mariä Himmelfahrt",
            f"{year}-11-01": "Allerheiligen",
            (easter + datetime.timedelta(days=60)).isoformat(): "Fronleichnam",
        },
        "Sachsen": {
            f"{year}-10-31": "Reformationstag",
            f"{year}-11-22": "Buß- und Bettag",
            (easter + datetime.timedelta(days=60)).isoformat(): "Fronleichnam",
        },
        "Sachsen-Anhalt": {
            f"{year}-01-06": "Heilige Drei Könige",
            f"{year}-10-31": "Reformationstag",
        },
        "Schleswig-Holstein": {f"{year}-10-31": "Reformationstag"},
        "Thüringen": {
            f"{year}-09-20": "Weltkindertag",
            f"{year}-10-31": "Reformationstag",
            (easter + datetime.timedelta(days=60)).isoformat(): "Fronleichnam",
        },
    }

    result = {**fixed, **movable}
    result.update(state_specific.get(state, {}))
    return result


# Sidebar
st.sidebar.write("""
Auf dieser Seite kann ich meine **Termine** dokumentieren und verwalten.

**Funktionen:**
- ➕ *Termin hinzufügen:* Über den Button **„+"** neue Termine eintragen.
- 📅 *Kalenderansicht:* Monatsübersicht mit Feiertagen und Terminen.
- 🗺️ *Bundesland:* Feiertage je nach Bundesland anzeigen.
""")

STATES = [
    "Baden-Württemberg",
    "Bayern",
    "Berlin",
    "Brandenburg",
    "Bremen",
    "Hamburg",
    "Hessen",
    "Mecklenburg-Vorpommern",
    "Niedersachsen",
    "Nordrhein-Westfalen",
    "Rheinland-Pfalz",
    "Saarland",
    "Sachsen",
    "Sachsen-Anhalt",
    "Schleswig-Holstein",
    "Thüringen",
]
selected_state = st.sidebar.selectbox(
    "🗺️ Bundesland", STATES, index=STATES.index("Nordrhein-Westfalen")
)

# Header
col1, buff, col2 = st.columns([0.4, 0.6, 0.07])
with col1:
    st.title("Kalender")
with col2:

    @st.dialog("📅 Termin hinzufügen")
    def add():
        show_event_form()

    st.write("")
    st.write("")
    if st.button("**+**"):
        add()

# Month navigation
today = datetime.date.today()
if "cal_year" not in st.session_state:
    st.session_state.cal_year = today.year
if "cal_month" not in st.session_state:
    st.session_state.cal_month = today.month

nav1, nav2, nav3 = st.columns([0.12, 0.76, 0.12])
with nav1:
    if st.button("◀", use_container_width=True):
        if st.session_state.cal_month == 1:
            st.session_state.cal_month = 12
            st.session_state.cal_year -= 1
        else:
            st.session_state.cal_month -= 1
        st.rerun()
with nav2:
    MONTHS_DE = [
        "Januar",
        "Februar",
        "März",
        "April",
        "Mai",
        "Juni",
        "Juli",
        "August",
        "September",
        "Oktober",
        "November",
        "Dezember",
    ]
    st.markdown(
        f"<h3 style='text-align:center;margin:0'>"
        f"{MONTHS_DE[st.session_state.cal_month - 1]} {st.session_state.cal_year}</h3>",
        unsafe_allow_html=True,
    )
with nav3:
    if st.button("▶", use_container_width=True):
        if st.session_state.cal_month == 12:
            st.session_state.cal_month = 1
            st.session_state.cal_year += 1
        else:
            st.session_state.cal_month += 1
        st.rerun()

# Load data
events = load_json("events/events.json")

year, month = st.session_state.cal_year, st.session_state.cal_month
holidays = get_holidays(year, selected_state)

# Group events by date — expand multi-day events across all days in range
events_by_date: dict[str, list] = {}
for ev in events:
    start = datetime.date.fromisoformat(ev["date"])
    end = datetime.date.fromisoformat(ev["end_date"]) if ev.get("end_date") else start
    current = start
    while current <= end:
        events_by_date.setdefault(current.isoformat(), []).append(ev)
        current += datetime.timedelta(days=1)

# Calendar CSS
st.markdown(
    """
<style>
.cal-grid { display:grid; grid-template-columns:repeat(7,1fr); gap:4px; margin-top:8px; }
.cal-header { text-align:center; font-weight:700; font-size:0.8rem;
              padding:6px 0; color:#888; text-transform:uppercase; letter-spacing:.05em; }
.cal-day {
    min-height:90px; border-radius:10px; padding:6px;
    background:#1e1e2e; border:1px solid #2a2a3e;
    font-size:0.78rem; position:relative; overflow:hidden;
}
.cal-day.today { border:2px solid #4f8ef7; background:#1a2540; }
.cal-day.other-month { opacity:0.35; }
.cal-day.holiday { background:#2a1f1f; border-color:#7a3030; }
.day-num { font-weight:700; font-size:0.85rem; margin-bottom:3px; }
.holiday-label { font-size:0.65rem; color:#e07070; margin-bottom:2px;
                 white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.event-chip {
    border-radius:4px; padding:1px 5px; margin-bottom:2px;
    font-size:0.65rem; white-space:nowrap; overflow:hidden;
    text-overflow:ellipsis; font-weight:600;
}
</style>
""",
    unsafe_allow_html=True,
)

# Build calendar HTML
cal = calendar.monthcalendar(year, month)
days_de = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]

html = '<div class="cal-grid">'
for d in days_de:
    html += f'<div class="cal-header">{d}</div>'

for week in cal:
    for day in week:
        if day == 0:
            html += '<div class="cal-day other-month"></div>'
            continue

        date_iso = f"{year}-{month:02d}-{day:02d}"
        is_today = day == today.day and month == today.month and year == today.year
        is_holiday = date_iso in holidays
        weekday = datetime.date(year, month, day).weekday()
        is_weekend = weekday >= 5

        classes = "cal-day"
        if is_today:
            classes += " today"
        if is_holiday:
            classes += " holiday"

        day_color = "#e07070" if is_weekend or is_holiday else "#cdd6f4"
        html += f'<div class="{classes}">'
        html += f'<div class="day-num" style="color:{day_color}">{day}</div>'

        if is_holiday:
            html += f'<div class="holiday-label">🎉 {holidays[date_iso]}</div>'

        for ev in events_by_date.get(date_iso, []):
            bg = ev.get("color", "#555")
            html += (
                f'<div class="event-chip" style="background:{bg}22;color:{bg};'
                f'border-left:3px solid {bg}">'
                f'{ev["title"]}</div>'
            )

        html += "</div>"

html += "</div>"
st.markdown(html, unsafe_allow_html=True)


@st.dialog("Event Details")
def show_event_details(event):
    st.write(f"**Titel:** {event['title']}")
    st.write(f"**Datum:** {event['date']}")
    st.write(f"**Beschreibung:** {event.get('desc', 'Keine Details')}")
    if st.button("Schließen"):
        st.rerun()


# Am Ende deiner App-Logik:
if "selected_event" in st.session_state:
    show_event_details(st.session_state.selected_event)
    del st.session_state.selected_event  # Zurücksetzen

# Legend
st.markdown("<br>", unsafe_allow_html=True)
legend_cols = st.columns(len(CATEGORY_COLORS))
for col, (cat, color) in zip(legend_cols, CATEGORY_COLORS.items()):
    col.markdown(
        f'<span style="background:{color}33;color:{color};border-left:3px solid {color};'
        f'padding:2px 8px;border-radius:4px;font-size:0.75rem;font-weight:600">{cat}</span>',
        unsafe_allow_html=True,
    )

# Event detail list for selected month
month_events = [e for e in events if e["date"].startswith(f"{year}-{month:02d}")]
if month_events:
    st.markdown("---")
    st.subheader("Termine dieses Monats")
    for ev in sorted(month_events, key=lambda x: (x["date"], x["time"])):
        color = ev.get("color", "#888")
        end_date_str = f" → {ev['end_date']}" if ev.get("end_date") else ""
        with st.expander(
            f"📌 {ev['date']}{end_date_str} · {ev['time']}–{ev['end_time']} Uhr · {ev['title']}"
        ):
            st.markdown(
                f'<span style="background:{color}33;color:{color};border-left:3px solid {color};'
                f'padding:2px 8px;border-radius:4px;font-size:0.75rem;font-weight:600">'
                f'{ev["category"]}</span>',
                unsafe_allow_html=True,
            )
            if ev.get("desc"):
                st.write(ev["desc"])
