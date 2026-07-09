import streamlit as st
import os

# Folder where files will be saved
UPLOAD_FOLDER = "files"

def upload_pdfs(label = "📄 Bewerbungen hochladen", isCV=False) -> None:
    """Handles uploading and saving PDF files to the 'files' folder."""

    # Ensure the folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # File uploader widget
    uploaded_files = st.file_uploader(
        label,
        type=['pdf'], 
        accept_multiple_files=True
    )

    # If user uploads files
    if uploaded_files:
        for uploaded_file in uploaded_files:
            if isCV:
                # Save file as "lebenslauf.pdf"
                save_path = os.path.join(UPLOAD_FOLDER, "lebenslauf.pdf")
            else:
                # Save with original filename
                save_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

            # Save the file
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.success(f"✅ '{os.path.basename(save_path)}' wurde gespeichert!")

        st.info(f"Alle Dateien wurden erfolgreich in '{UPLOAD_FOLDER}' gespeichert.")
