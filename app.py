from login import login_interface

login_interface()  # Show sidebar login prompt

if st.session_state["is_admin"]:
    st.sidebar.markdown("✅ Admin access granted")
    # Show admin tools or exports here

