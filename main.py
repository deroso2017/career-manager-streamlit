from pathlib import Path
import streamlit as st

# App paths
dir_path = Path(__file__).parent
PROFILE_IMAGE = dir_path / "files" / "profile.jpg"

# Set your password here
PASSWORD = "715D111777" 

def login():
    """
    Display a password input form for the user.
    Returns True if the password is correct.
    """
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # Only show login form if not logged in
    if not st.session_state.logged_in:
        st.title("🔒 Bitte geben Sie das Passwort ein, um fortzufahren.")
        password_input = st.text_input("Password", type="password", key="pw_input")
        if st.button("Login"):
            if password_input == PASSWORD:
                st.session_state.logged_in = True
                st.success("✅ Passwort korrekt! Willkommen!")
                st.rerun()  # refresh app so login form disappears
            else:
                st.error("❌ Falsches Passwort. Bitte versuchen Sie es erneut.")
        return False
    else:
        # Already logged in
        return True

def run() -> None:
    """
    Main function to set up and run the Streamlit app with navigation.
    """
    # First, check login
    if not login():
        return  # Stop running the rest of the app until password is correct

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
                    dir_path / "pages" / "activities.py",
                    title="Aktivitäten",
                    icon=":material/browse_activity:",
                ),
                st.Page(
                    dir_path / "pages" / "about_me.py",
                    title="Über mich",
                    icon=":material/contact_page:",
                ),
                # st.Page(
                #     dir_path / "temp.py",
                #     title="temp",
                #     icon=":material/settings:",
                # ),
            ]
        }
    )

    # Run selected page
    page.run()


if __name__ == "__main__":
    run()
