import base64
import io
import streamlit as st
from pathlib import Path
from components.pdf_preview import show_pdf_preview

st.set_page_config(page_title="Über mich", page_icon=":material/contact_page:")
st.title("Über mich")

img_path = Path("files/profile-img.png")
pdf_path = Path("files/lebenslauf.pdf")

# --- Sidebar with circular profile image ---
with open(img_path, "rb") as img_file:
        img_bytes = img_file.read()
        img_base64 = base64.b64encode(img_bytes).decode()
        img_src = f"data:image/png;base64,{img_base64}"

with st.sidebar:
        # Add custom CSS to make Streamlit image circular
        st.markdown(
            """
            <style>
            .profile-pic {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                object-fit: cover;
                border: 3px solid #4CAF50;
                display: block;
                margin-left: auto;
                margin-right: auto;
            }
            .profile-container {
                text-align: center;
                margin-bottom: 1.5rem;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        

        # Wrap the image in a link (clickable)
        st.markdown(
            f"""
            <div class="profile-container">
                    <img src="{img_src}" class="profile-pic" />
                <p><b>Behdad Tabrizi</b></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

if pdf_path.exists():
    with open(pdf_path, "rb") as f:
        uploaded_file = io.BytesIO(f.read())

    show_pdf_preview(uploaded_file, pages=3, show_button= False, show_page_label= False) 
else:
    st.warning("PDF file not found!")