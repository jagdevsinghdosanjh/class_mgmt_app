import streamlit as st

# Import view modules
from views.dashboard import student_dashboard
from views.fee_view import fee_view
from views.admin_tools import patch_fee_ledgers_streamlit

# Import login system
from login import login_interface

# Initialize admin session state
if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False

# Sidebar branding & login
st.sidebar.image("assets/logo.png", width=150)
st.sidebar.title("Class Manager 🧮")
login_interface()  # Admin login sidebar

# App Header
st.title("📘 Class Management System")

# Navigation tabs based on login status
tabs = ["Dashboard", "Fee Ledger"]
if st.session_state["is_admin"]:
    tabs.append("Admin Tools")

selected_tab = st.sidebar.radio("Navigate", tabs)

# Tab routing
if selected_tab == "Dashboard":
    student_dashboard()
elif selected_tab == "Fee Ledger":
    fee_view()
elif selected_tab == "Admin Tools":
    patch_fee_ledgers_streamlit()





# from login import login_interface

# login_interface()  # Show sidebar login prompt

# if st.session_state["is_admin"]:
#     st.sidebar.markdown("✅ Admin access granted")
#     # Show admin tools or exports here

