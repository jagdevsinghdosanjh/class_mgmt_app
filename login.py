import streamlit as st
import hashlib

# User database simulation (use MongoDB later if needed)
USER_CREDENTIALS = {
    "admin": hashlib.sha256("password123".encode()).hexdigest()
}

def login_interface():
    st.sidebar.subheader("🔐 Admin Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    
    if st.sidebar.button("Login"):
        hashed = hashlib.sha256(password.encode()).hexdigest()
        if USER_CREDENTIALS.get(username) == hashed:
            st.session_state["is_admin"] = True
            st.success("Welcome, Admin 👋")
        else:
            st.error("Invalid credentials")

# Initialize session state (can also be done in app.py once)
if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False
