import streamlit as st
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher

# User info
names = ["Max Mustermann", "Anna Beispiel"]
usernames = ["max", "anna"]
passwords = ["pass123", "securepwd"]

# Hash passwords safely
hashed_pw = Hasher.hash_list(passwords)

credentials = {
    "usernames": {
        usernames[i]: {"name": names[i], "password": hashed_pw[i]}
        for i in range(len(usernames))
    }
}

# Create authenticator
authenticator = stauth.Authenticate(
    credentials,
    cookie_name="auth_cookie_name",
    key="auth_signature_key",
    cookie_expiry_days=1
)
