import streamlit as st

# Import views
from views.dashboard import student_dashboard
from views.fee_view import fee_view
from views.admin_tools import admin_tools_panel
from login import login_interface

# Initialize admin session
if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False

# Sidebar login
st.sidebar.image("assets/logo.png", width=150)
st.sidebar.title("Class Manager 🧮")
login_interface()

# Header
st.title("📘 Class Management System")

# Navigation
tabs = ["Dashboard", "Fee Ledger"]
if st.session_state["is_admin"]:
    tabs.append("Admin Tools")

selected_tab = st.sidebar.radio("Navigate", tabs)

# Routing
if selected_tab == "Dashboard":
    student_dashboard()
elif selected_tab == "Fee Ledger":
    fee_view()
elif selected_tab == "Admin Tools":
    admin_tools_panel()
