import streamlit as st

from views.dashboard import student_dashboard
from views.fee_view import fee_view
from views.admin_tools import admin_tools_panel
from login import login_interface

if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False

st.sidebar.image("assets/logo.png", width=150)
st.sidebar.title("Class Manager 🧮")
login_interface()

st.title("📘 Class Management System")

tabs = ["Dashboard", "Fee Ledger"]
if st.session_state["is_admin"]:
    tabs.append("Admin Tools")

selected_tab = st.sidebar.radio("Navigate", tabs)

if selected_tab == "Dashboard":
    student_dashboard()
elif selected_tab == "Fee Ledger":
    fee_view()
elif selected_tab == "Admin Tools" and st.session_state["is_admin"]:
    admin_tools_panel()
