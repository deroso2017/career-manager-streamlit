import json
import calendar
import locale
import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path

# Path to your JSON file
DATA_FILE = Path("files/applications.json")

# Load JSON data
if DATA_FILE.exists():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        applications_list = json.load(f)
else:
    st.error("JSON file not found!")
    applications_list = []

st.set_page_config(page_title="Dashboard", page_icon=":material/dashboard:")
st.title("Dashboard")
st.markdown(
    """
    <h3>Wo ich mich aktuell bewerbe:</h3>

    <ul>
        <li><a href="https://www.linkedin.com" style="color:#33E6B3;" target="_blank">LinkedIn</a></li>
        <li><a href="https://web.arbeitsagentur.de/" style="color:#33E6B3;" target="_blank">Arbeitsagentur</a></li>
        <li><a href="https://www.stepstone.de" style="color:#33E6B3;" target="_blank">Stepstone</a></li>
        <li><a href="https://join.com/talent/applications" style="color:#33E6B3;" target="_blank">Join</a></li>
        <li><a href="https://www.instaffo.com/en/talent" style="color:#33E6B3;" target="_blank">Instaffo</a></li>
    </ul>
    """,
    unsafe_allow_html=True
)

st.subheader("📊 Bewerbungen nach Jahr")

if applications_list:
    locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
    # Convert to DataFrame
    df_apps = pd.DataFrame(applications_list)
    df_apps['date'] = pd.to_datetime(df_apps['date'])
    df_apps['year'] = df_apps['date'].dt.year.astype(str)
    df_apps['month'] = df_apps['date'].dt.strftime('%B')  # Full month name

    # Aggregate counts per year and month
    applications = df_apps.groupby(['year', 'month']).size().unstack(fill_value=0).to_dict('index')

    # Select year
    selected_year = st.selectbox("Jahr", list(applications.keys()))
    data = applications[selected_year]

    df_plot = pd.DataFrame(list(data.items()), columns=["Monat", "Bewerbungen"])

    # Assign colors: largest value gets #33CC99, others get different colors
    base_colors = ["#7030A0", "#007A6E", "#FFD9A0", "#FF705A"]
    colors = []
    max_index = df_plot["Bewerbungen"].idxmax()

    for i in range(len(df_plot)):
        if i == max_index:
            colors.append("#33E6B3")
        else:
            colors.append(base_colors[i % len(base_colors)])

    df_plot["color"] = colors
    

    # Define month order
    month_order = list(calendar.month_name)[1:]  # ['January', 'February', ..., 'December']
    # Convert 'Monat' to categorical with proper order
    df_plot['Monat'] = pd.Categorical(df_plot['Monat'], categories=month_order, ordered=True)

    # Now when we plot, months will appear chronologically
    chart = alt.Chart(df_plot).mark_bar().encode(
        x=alt.X("Monat", sort=month_order),
        y="Bewerbungen",
        color=alt.Color("color", scale=None)
    )

    st.altair_chart(chart, use_container_width=True)
