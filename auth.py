import streamlit as st

def require_login():
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.warning("🔒 Bitte zuerst einloggen.")
        st.switch_page("main.py")  # change to your main file name
        st.stop()
