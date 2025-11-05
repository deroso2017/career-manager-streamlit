import streamlit as st
import datetime

from components.pdf_preview import show_pdf_preview
from pathlib import Path
import io

st.subheader("Dialog")
@st.dialog("Hochladen")
def vote(item):
    st.write(f"Why is {item} your favorite?")
    reason = st.text_input("Because...")
    if st.button("Submit"):
        st.session_state.vote = {"item": item, "reason": reason}
        st.rerun()

if "vote" not in st.session_state:
    st.write("Vote for your favorite")
    if st.button("A"):
        vote("A")
    if st.button("B"):
        vote("B")
else:
    f"You voted for {st.session_state.vote['item']} because {st.session_state.vote['reason']}"

st.divider()

st.subheader("Datepicker")
# date input widget
d = st.date_input("When's your birthday", datetime.date(2019, 7, 6))
st.write("Your birthday is:", d)

st.divider()

st.subheader("pdf preview ")

# Path to your local PDF
pdf_path = Path("files/Yahoo Mail - Ihre Bewerbung als Frontend Developer (m_f_d) bei PALTRON.pdf")

if pdf_path.exists():
    with open(pdf_path, "rb") as f:
        uploaded_file = io.BytesIO(f.read())

    show_pdf_preview(uploaded_file, pages=2)  # show first page only
else:
    st.warning("PDF file not found!")

# show_pdf_preview(uploaded_file, pages=1)

st.divider()

from components.add_application import show_application_form

st.title("📂 Job Applications App")

show_application_form()
