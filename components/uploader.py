import streamlit as st
from storage import upload_file


def upload_pdfs(label="📄 Bewerbungen hochladen", isCV=False) -> None:
    is_admin = st.session_state.get("is_admin", False)

    if not is_admin:
        st.button(label, disabled=True, use_container_width=True)
        st.info("🔒 Nur der Entwickler kann Dateien hochladen.")
        return

    uploaded_files = st.file_uploader(label, type=["pdf"], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            key = "files/lebenslauf.pdf" if isCV else f"files/{uploaded_file.name}"
            upload_file(uploaded_file.getvalue(), key)
            st.success(f"✅ '{key.split('/')[-1]}' wurde gespeichert!")
            st.rerun()
