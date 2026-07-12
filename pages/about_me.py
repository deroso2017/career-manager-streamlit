import base64
import io
import streamlit as st
from components.pdf_preview import show_pdf_preview
from components.uploader import upload_pdfs
from auth import require_login
from storage import download_file, file_exists

require_login()

st.set_page_config(page_title="Über mich", page_icon=":material/contact_page:")
st.title("Über mich")

with open("files/profile-img.png", "rb") as img_file:
    img_src = f"data:image/png;base64,{base64.b64encode(img_file.read()).decode()}"

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

    st.sidebar.write("""
Diese Seite präsentiert meine **persönlichen Informationen** und meinen **Lebenslauf**.  
                 
*Funktionen:*
- 📄 *Lebenslauf-Vorschau:* 
  Eine integrierte PDF-Vorschau zeigt meinen Lebenslauf direkt auf der Seite.
- ⬆️ *Lebenslauf hochladen:*
  Falls noch kein PDF vorhanden ist, kann ich meinen aktuellen Lebenslauf direkt hochladen.
""")

if file_exists("files/lebenslauf.pdf"):
    with st.spinner("Lade Daten..."):
        pdf_bytes = download_file("files/lebenslauf.pdf")
        show_pdf_preview(
            io.BytesIO(pdf_bytes), pages=3, show_button=False, show_page_label=False
        )
else:
    st.warning("PDF file not found!")
    upload_pdfs(label="Lebenslauf hochladen", isCV=True)
