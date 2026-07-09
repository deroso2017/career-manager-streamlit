import os
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# App paths
dir_path = Path(__file__).parent
PROFILE_IMAGE = dir_path / "files" / "profile.jpg"
LOGIN_BACKGROUND = dir_path / "files" / "login_background.png"

PASSWORD = os.getenv("PASSWORD")


# --- Info Popup ---
@st.dialog("ℹ️ Über dieses Projekt")
def show_project_info():
    st.markdown("""
        Diese App wurde als **Testprojekt** entwickelt,  
        um die Grundlagen von **Python** und dem **Streamlit Framework** praktisch anzuwenden.  

        Ich habe sie parallel zu meinen Grundlagen-Python-Kursen, die ich selbstständig gelernt habe, erstellt,
        um das Gelernte umzusetzen und zu veröffentlichen.

        ---
        🧠 **Technologien:**  
        - Python  
        - Streamlit  
        - JSON / Pandas / Altair  

        📂 **Zweck:**  
        Demonstration einer vollständigen, interaktiven Anwendung –  
        von Datenverwaltung über Visualisierung bis hin zur Benutzeroberfläche.       
    """)


def hide_sidebar():
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {display: none;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def login():
    """
    Display a password input form for the user.
    Returns True if the password is correct.
    """

    # --- Initialize session state variables ---
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "info_shown" not in st.session_state:
        st.session_state.info_shown = False
    if "show_popup_next" not in st.session_state:
        st.session_state.show_popup_next = False

    # --- Show login form if not yet logged in ---
    if not st.session_state.logged_in:
        set_login_background()
        st.title("🔒 Bitte geben Sie das Passwort ein, um fortzufahren.")
        password_input = st.text_input("Passwort", type="password", key="pw_input")

        if st.button("App starten", use_container_width=True):
            if password_input == PASSWORD:
                st.session_state.logged_in = True
                st.success("✅ Passwort korrekt! Willkommen!")

                # Note that the pop-up should be opened during the next run.
                if not st.session_state.info_shown:
                    st.session_state.show_popup_next = True

                st.rerun()  # Reload -> removes the form
            else:
                st.error("❌ Falsches Passwort. Bitte versuchen Sie es erneut.")
        return False

    else:
        # --- If already logged in ---
        # If a popup should be displayed after login
        if st.session_state.show_popup_next and not st.session_state.info_shown:
            show_project_info()
            st.session_state.info_shown = True
            st.session_state.show_popup_next = False

        return True


def set_login_background():
    """
    Set a background image for the login screen.
    """
    if LOGIN_BACKGROUND.exists():
        with open(LOGIN_BACKGROUND, "rb") as image_file:
            import base64

            encoded_image = base64.b64encode(image_file.read()).decode()

        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: linear-gradient(
                    rgba(0, 0, 0, 0.55),
                    rgba(0, 0, 0, 0.55)
                ),
                url("data:image/jpg;base64,{encoded_image}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}

            .block-container {{
                background-color: rgba(255, 255, 255, 0.08);
                border-radius: 15px;
                padding: 2rem;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )


def run() -> None:
    """Main function to set up and run the Streamlit app with navigation."""

    # Check login first
    if not login():
        hide_sidebar()
        return

    # Navigation pages
    page = st.navigation(
        {
            "": [
                st.Page(
                    dir_path / "pages" / "dashboard.py",
                    title="Dashboard",
                    icon=":material/dashboard:",
                ),
                st.Page(
                    dir_path / "pages" / "applications.py",
                    title="Bewerbungen",
                    icon=":material/assignment:",
                ),
                st.Page(
                    dir_path / "pages" / "job_search.py",
                    title="Jobbörse",
                    icon=":material/search:",
                ),
                st.Page(
                    dir_path / "pages" / "activities.py",
                    title="Aktivitäten",
                    icon=":material/browse_activity:",
                ),
                st.Page(
                    dir_path / "pages" / "about_me.py",
                    title="Über mich",
                    icon=":material/contact_page:",
                ),
            ]
        }
    )

    page.run()


if __name__ == "__main__":
    run()
