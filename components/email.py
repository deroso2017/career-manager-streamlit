import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

CONTACT_EMAIL = os.getenv("CONTACT_EMAIL")


def show_email_button():
    email_address = CONTACT_EMAIL

    st.markdown(
        f"""
        <style>
            #email-btn {{ 
                position: fixed; 
                bottom: 64px; 
                right: 24px; 
                width: 52px; 
                height: 52px; 
                border-radius: 50%; 
                background: #33E6B3; 
                border: none; 
                cursor: pointer; 
                box-shadow: 0 4px 16px rgba(51,230,179,0.4); 
                display: flex; 
                align-items: center; 
                justify-content: center; 
                z-index: 999999; 
                text-decoration: none;
            }}
            #email-btn:hover {{
                box-shadow: 0 6px 20px rgba(51,230,179,0.6);
            }}
        </style>

        <a href="mailto:{email_address}" id="email-btn" title="E-Mail senden">
            <svg viewBox="0 0 24 24" width="24" height="24" fill="#0e1117">
                <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
            </svg>
        </a>
        """,
        unsafe_allow_html=True,
    )


show_email_button()
