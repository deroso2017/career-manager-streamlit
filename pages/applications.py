import streamlit as st
import pandas as pd
from components.add_application import show_application_form
from auth import require_login
from storage import load_json, download_file

require_login()

# Reset download states on fresh page navigation
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

col1, buff, col2 = st.columns([0.4, 0.3, 0.14])
with col1:
    st.title("Bewerbungen")
with col2:

    @st.dialog("📂 Bewerbung")
    def add():
        show_application_form()

    st.write("")
    st.write("")
    if st.button("Hochladen"):
        add()

# --- Load data safely ---
applications = load_json("applications/applications.json")
if not applications:
    st.warning("⚠️ Keine Bewerbungsdaten gefunden.")
    st.stop()

# Convert to DataFrame
df = pd.DataFrame(applications)

# --- Ensure 'date' column exists ---
if "date" not in df.columns:
    st.error("❌ Spalte 'date' fehlt in der JSON-Datei.")
    st.stop()

# --- Prepare columns ---
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["month_num"] = df["date"].dt.month

# Add year and month
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
df["year"] = df["date"].dt.year.astype("Int64").astype(str)
df["month"] = df["date"].dt.month.apply(
    lambda m: months_de[m - 1] if pd.notna(m) and 1 <= m <= 12 else None
)

# --- Select year ---
years = sorted(df["year"].dropna().unique(), reverse=True)
selected_year = st.selectbox("Jahr", years)

# --- Filter and Sort (Chronological: Newest to Oldest) ---
df_year = df[df["year"] == selected_year].copy()
df_year = df_year.sort_values(by="date", ascending=False)

# --- Group data for Chart ---
monthly_counts = (
    df_year.groupby("month_num")
    .size()
    .reindex(range(1, 13), fill_value=0)  # alle Monate in korrekter Reihenfolge
)
monthly_counts_nonzero = monthly_counts[monthly_counts > 0]

# Map month numbers back to German names for the chart labels
if len(monthly_counts_nonzero) > 0:
    monthly_counts_nonzero.index = [
        months_de[m - 1] for m in monthly_counts_nonzero.index
    ]

# --- Show Data Table ---
st.subheader(f"📅 Bewerbungen im Jahr {selected_year}")

# Copy for formatting so we don't break datetime sorting
df_display = df_year.copy()
df_display["date_str"] = df_display["date"].dt.strftime("%d.%m.%Y")

st.dataframe(
    df_display[["company", "date_str", "status", "platform"]]
    .rename(
        columns={
            "company": "Firma",
            "date_str": "Datum",
            "status": "Status",
            "platform": "Plattform",
        }
    )
    .reset_index(drop=True)
    .rename_axis(None)
    .rename(lambda x: x + 1)
)

# --- Show bar chart (with multi-color months) ---
if len(monthly_counts_nonzero) > 0:
    if isinstance(monthly_counts_nonzero.index[0], str):
        month_names = list(monthly_counts_nonzero.index)
    else:
        month_names = [months_de[int(m) - 1] for m in monthly_counts_nonzero.index]
    month_values = monthly_counts_nonzero.values
else:
    month_names = []
    month_values = []

# Build DataFrame for chart
chart_data = pd.DataFrame({"Monat": month_names, "Bewerbungen": month_values})

# Keep months in correct calendar order (Jan–Dez)
chart_data["Monat"] = pd.Categorical(
    chart_data["Monat"], categories=months_de, ordered=True
)
chart_data = chart_data.sort_values("Monat")

st.subheader(f"📊 Bewerbungen pro Monat ({selected_year})")

# Hier nutzen wir color="Monat" für unterschiedliche Farben pro Balken
st.bar_chart(data=chart_data, x="Monat", y="Bewerbungen", color="Monat")


st.divider()


# --- Downloads Area (Modernized UI) ---
downloads_expander = st.expander("📥 Dokumente Herunterladen")

with downloads_expander:
    # Filter out empty paths
    df_downloads = df_year[df_year["link"].notna() & (df_year["link"] != "")].copy()

    if df_downloads.empty:
        st.info("Keine Dokumente für dieses Jahr verfügbar.")
    else:
        # Subtle, modern header context (optional, since card layouts are self-explanatory)
        st.markdown(
            "<small style='color: gray;'>Verfügbare Dokumente für den Download:</small>",
            unsafe_allow_html=True,
        )

        for idx, row in df_downloads.iterrows():
            # Container with borders creates a clean card UI for each document row
            with st.container(border=True):
                # Native vertical alignment keeps elements perfectly centered
                col_date, col_company, col_btn = st.columns(
                    [0.2, 0.5, 0.3], vertical_alignment="center"
                )

                with col_date:
                    # Sleek, muted date token appearance
                    st.caption(f"🗓️ {row['date'].strftime('%d.%m.%Y')}")

                with col_company:
                    # Clean bold typography
                    st.markdown(f"**{row['company']}**")

                with col_btn:
                    file_path = row["link"]
                    filename = file_path.split("/")[-1]

                    btn_key = f"btn_{idx}"
                    dl_key = f"dl_{idx}"
                    file_key = f"file_{idx}"
                    is_ready = st.session_state.get(f"ready_{idx}", False)

                    if not is_ready:
                        if st.button(
                            "Bereitstellen",
                            icon="📥",
                            key=btn_key,
                            use_container_width=True,
                            type="secondary",
                        ):
                            try:
                                with st.spinner("Lade Datei..."):
                                    st.session_state[file_key] = download_file(file_path)
                                st.session_state[f"ready_{idx}"] = True
                            except Exception:
                                st.error("Fehler beim Laden")
                            st.rerun()
                    else:
                        clicked = st.download_button(
                            label="Speichern",
                            icon="💾",
                            data=st.session_state[file_key],
                            file_name=filename,
                            mime="application/octet-stream",
                            key=dl_key,
                            use_container_width=True,
                            type="primary",
                        )
                        if clicked:
                            st.session_state[f"ready_{idx}"] = False
                            del st.session_state[file_key]
                            st.rerun()
