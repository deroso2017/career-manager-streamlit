import base64
import json
import streamlit as st
import pandas as pd
from pathlib import Path
from components.add_application import show_application_form

st.set_page_config(page_title="Bewerbungen", page_icon=":material/show_chart:")
col1, buff, col2 = st.columns([.4, .4, .2])
with col1:
    st.title("Bewerbungen")
with col2:
    @st.dialog("📂 Job Applications App")
    def add():
        show_application_form()
        
    st.write("")
    st.write("")
    if st.button("Hochladen"):
        add()
        
DATA_FILE = Path("files/applications.json")
# --- Load data safely ---
if not DATA_FILE.exists():
    st.error("❌ Datei 'applications.json' wurde nicht gefunden.")
    st.stop()

try:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        applications = json.load(f)
except json.JSONDecodeError:
    st.error("⚠️ Fehler beim Lesen der JSON-Datei. Bitte prüfen Sie die Formatierung.")
    st.stop()

# --- Ensure correct structure ---
if not isinstance(applications, list) or len(applications) == 0:
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
    "Januar","Februar","März","April","Mai","Juni",
    "Juli","August","September","Oktober","November","Dezember"
]
df["year"] = df["date"].dt.year.astype("Int64").astype(str)
df["month"] = df["date"].dt.month.apply(
    lambda m: months_de[m-1] if pd.notna(m) and 1 <= m <= 12 else None
)

# --- Select year ---
years = sorted(df["year"].dropna().unique())
selected_year = st.selectbox("Jahr", years)

# --- Filter and group ---
df_year = df[df["year"] == selected_year].copy()
monthly_counts = (
    df_year.groupby("month_num").size()
    .reindex(range(1, 13), fill_value=0)   # alle Monate in korrekter Reihenfolge
)
# optional: nur Monate mit >0 Anzeigen (falls gewünscht)
monthly_counts_nonzero = monthly_counts[monthly_counts > 0]

# Map month numbers back to German names for the chart labels
monthly_counts_nonzero.index = [months_de[m-1] for m in monthly_counts_nonzero.index]

# --- Show data ---
st.subheader(f"📅 Bewerbungen im Jahr {selected_year}")
df_year["date"] = df_year["date"].dt.strftime("%d.%m.%Y")
st.dataframe(
    df_year[["company" , "date", "status", "platform"]]
    .rename(columns={"company": "Firma", "date": "Datum", "status": "Status", "platform": "Plattform"})
    .reset_index(drop=True)
    .rename_axis(None)
    .rename(lambda x: x + 1)
)

# --- Show bar chart (keep chronological order) ---

# Detect whether index contains month numbers or month names
if isinstance(monthly_counts_nonzero.index[0], str):
    # index already has names like "August", "September", ...
    month_names = list(monthly_counts_nonzero.index)
    month_values = monthly_counts_nonzero.values
else:
    # index has numeric month numbers (1–12)
    month_names = [months_de[int(m) - 1] for m in monthly_counts_nonzero.index]
    month_values = monthly_counts_nonzero.values

# Build DataFrame for chart
chart_data = pd.DataFrame({
    "Monat": month_names,
    "Bewerbungen": month_values
})

# Keep months in correct calendar order (Jan–Dez)
chart_data["Monat"] = pd.Categorical(chart_data["Monat"], categories=months_de, ordered=True)
chart_data = chart_data.sort_values("Monat")

st.subheader(f"📊 Bewerbungen pro Monat ({selected_year})")
st.bar_chart(data=chart_data, x="Monat", y="Bewerbungen")


st.divider()

def make_download_link(file_path):
    file_path = Path(file_path)
    if not file_path.exists():
        return "❌"
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    b64 = base64.b64encode(file_bytes).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_path.name}">📥</a>'
    return href

df_year["Download"] = df_year["link"].apply(make_download_link)

# Select visible columns
display_cols = ["company", "date", "Download"]

# Convert to HTML without header
table_html = df_year[display_cols].to_html(index=False, header=False, escape=False)

# Add CSS for full width
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

# Display in expander
downloads_expander = st.expander("Herunterladen")
downloads_expander.markdown(full_width_html, unsafe_allow_html=True)



