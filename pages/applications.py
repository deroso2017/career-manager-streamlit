import streamlit as st
import pandas as pd
from components.add_application import show_application_form
from auth import require_login
from storage import load_json, download_file

require_login()

# Reset download states
if not st.session_state.get("_on_apps_page"):
    for key in list(st.session_state.keys()):
        if key.startswith("ready_") or key.startswith("file_"):
            del st.session_state[key]
st.session_state["_on_apps_page"] = True

st.set_page_config(page_title="Bewerbungen", page_icon=":material/show_chart:")

st.sidebar.write(""" 
Diese Seite zeigt eine detaillierte Übersicht aller erfassten Bewerbungen.  
Hier kann ich **neue Bewerbungen hochladen**, vorhandene Einträge durchsuchen und monatliche Aktivitäten analysieren.

**Funktionen:**
- 📂 *Bewerbung hinzufügen:* Über den Button *„Hochladen“* kann ich neue Bewerbungen direkt eintragen.
- 📅 *Jahresauswahl:* Wähle ein Jahr aus, um nur Bewerbungen dieses Jahres anzuzeigen.
- 📊 *Monatliche Statistik* - 📥 *Downloads:* Im unteren Bereich kann ich Bewerbungsdokumente direkt herunterladen.
""")


# --- Modals ---
@st.dialog("📂 Bewerbung")
def open_form(data=None):
    show_application_form(edit_data=data)


# --- UI Layout ---
col1, buff, col2 = st.columns([0.4, 0.3, 0.14])
with col1:
    st.title("Bewerbungen")
with col2:
    st.write("")
    st.write("")
    if st.button("Hochladen"):
        open_form()

# --- Load and Prepare Data ---
applications = load_json("applications/applications.json")
if not applications:
    st.warning("⚠️ Keine Bewerbungsdaten gefunden.")
    st.stop()

df = pd.DataFrame(applications)
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["year"] = df["date"].dt.year.astype("Int64").astype(str)

years = sorted(df["year"].dropna().unique(), reverse=True)
selected_year = st.selectbox("Jahr", years)

df_year = (
    df[df["year"] == selected_year]
    .sort_values(by="date", ascending=False)
    .reset_index(drop=True)
)

# --- Display: Pandas Table ---
st.subheader(f"📅 Bewerbungen im Jahr {selected_year}")

df_display = df_year.copy()
df_display["date_str"] = df_display["date"].dt.strftime("%d.%m.%Y")
st.dataframe(
    df_display[["company", "date_str", "status", "platform"]].rename(
        columns={
            "company": "Firma",
            "date_str": "Datum",
            "status": "Status",
            "platform": "Plattform",
        }
    ),
    use_container_width=True,
    hide_index=True,
)

# --- Edit Logic (via Selection) ---
with st.expander("✏️ Eintrag bearbeiten"):
    options = {
        f"{row['company']} ({row['date'].strftime('%d.%m.%Y')})": i
        for i, row in df_year.iterrows()
    }
    selection = st.selectbox("Wähle eine Bewerbung zur Bearbeitung:", options.keys())
    if st.button("Auswahl öffnen"):
        idx = options[selection]
        row_dict = df_year.iloc[idx].to_dict()
        row_dict["date"] = df_year.iloc[idx]["date"].strftime("%Y-%m-%d")
        open_form(data=row_dict)

st.divider()

# --- Bar Chart (Original Style) ---
months_de = [
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
monthly_counts = (
    df_year.groupby(df_year["date"].dt.month).size().reindex(range(1, 13), fill_value=0)
)
monthly_counts_nonzero = monthly_counts[monthly_counts > 0]
chart_data = pd.DataFrame(
    {
        "Monat": [months_de[m - 1] for m in monthly_counts_nonzero.index],
        "Bewerbungen": monthly_counts_nonzero.values,
    }
)
chart_data["Monat"] = pd.Categorical(
    chart_data["Monat"], categories=months_de, ordered=True
)
chart_data = chart_data.sort_values("Monat")

st.subheader(f"📊 Bewerbungen pro Monat ({selected_year})")
st.bar_chart(data=chart_data, x="Monat", y="Bewerbungen", color="Monat")

st.divider()

# --- Downloads ---
downloads_expander = st.expander("📥 Dokumente Herunterladen")
with downloads_expander:
    df_downloads = df_year[df_year["link"].notna() & (df_year["link"] != "")]
    if df_downloads.empty:
        st.info("Keine Dokumente für dieses Jahr verfügbar.")
    else:
        for idx, row in df_downloads.iterrows():
            with st.container(border=True):
                c_date, c_comp, c_btn = st.columns(
                    [0.2, 0.5, 0.3], vertical_alignment="center"
                )
                c_date.caption(f"🗓️ {row['date'].strftime('%d.%m.%Y')}")
                c_comp.markdown(f"**{row['company']}**")

                file_key = f"file_{idx}"
                if not st.session_state.get(f"ready_{idx}"):
                    if c_btn.button(
                        "Bereitstellen",
                        icon="📥",
                        key=f"btn_{idx}",
                        use_container_width=True,
                    ):
                        st.session_state[file_key] = download_file(row["link"])
                        st.session_state[f"ready_{idx}"] = True
                        st.rerun()
                else:
                    if c_btn.download_button(
                        "Speichern",
                        icon="💾",
                        data=st.session_state[file_key],
                        file_name=row["link"].split("/")[-1],
                        key=f"dl_{idx}",
                        use_container_width=True,
                    ):
                        st.session_state[f"ready_{idx}"] = False
                        st.rerun()
