import base64
import streamlit as st
import pandas as pd
from components.add_application import show_application_form
from auth import require_login
from storage import load_json, download_file

require_login()

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


# --- Downloads Area (HTML Table + Pure On-Demand Fetching) ---

# 1. Catch if the user just clicked one of your HTML links
query_params = st.query_params
if "download_idx" in query_params:
    target_idx = int(query_params["download_idx"])

    # Locate the single requested file row safely
    matched_row = df[df.index == target_idx]
    if not matched_row.empty:
        file_path = matched_row["link"].values[0]
        filename = file_path.split("/")[-1]

        with st.spinner("Datei wird abgerufen..."):
            try:
                # ONLY downloads the file from B2 at this specific moment!
                file_bytes = download_file(file_path)
                b64 = base64.b64encode(file_bytes).decode()

                # Automatically trigger the browser download payload and wipe the URL clean
                st.html(f"""
                    <a id="auto_dl" href="data:application/octet-stream;base64,{b64}" download="{filename}" style="display:none;"></a>
                    <script>
                        document.getElementById('auto_dl').click();
                        window.history.replaceState({{}}, '', window.location.pathname);
                    </script>
                """)
                st.query_params.clear()
                st.rerun()
            except Exception:
                st.error("Fehler beim Herunterladen der Datei.")


# 2. Render your exact original full-width table layout
def make_dynamic_download_link(row_idx, file_path):
    if pd.isna(file_path) or not file_path:
        return "❌"
    # The link reloads the page with a targeted target parameter, preventing global loading lag
    return f'<a href="?download_idx={row_idx}" target="_self">📥</a>'


# Apply the dynamic indexing trick to your original rows
df_year["Download"] = [
    make_dynamic_download_link(idx, row["link"]) for idx, row in df_year.iterrows()
]
df_year["date_formatted"] = df_year["date"].dt.strftime("%d.%m.%Y")

# Select visible columns for the clean HTML Table
df_html = df_year[["company", "date_formatted", "Download"]].copy()

# Convert to HTML without header
table_html = df_html.to_html(index=False, header=False, escape=False)

# Add CSS for full width (Your original exact style)
full_width_html = f"""
<style>
table {{
    width: 100%;
    border-collapse: collapse;
}}
td {{
    padding: 8px;
    text-align: left;
}}
</style>
{table_html}
"""

# Display in expander exactly like before
downloads_expander = st.expander("Herunterladen")
downloads_expander.markdown(full_width_html, unsafe_allow_html=True)
