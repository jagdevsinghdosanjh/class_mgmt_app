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
    st.session_state.setdefault("user_id",None)
    st.session_state.setdefault("selected_student", None)

#Init Session is a clean way to centralize your session state setup in Streamlit

def init_session_keys():
    default_state = {
        "is_admin": False,
        "user_id": None,
        "selected_student": None,
        "selected_month": None,
        "student_map": {},             # optional: cache for performance
        "email_status": None,         # can be used to show success/fail after sending
        "sms_status": None,           # likewise
        "session_initialized": True   # flag to prevent reinitialization
    }

    for key, value in default_state.items():
        if key not in st.session_state:
            st.session_state[key] = value
    

# Other Essentials
    init_session_keys()
