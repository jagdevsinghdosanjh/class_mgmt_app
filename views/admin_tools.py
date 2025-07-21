import streamlit as st
from communication import send_email_receipt, send_sms
import os

def patch_fee_ledgers_streamlit():
    st.subheader("🩺 Fix Fee Ledgers")
    if st.button("🔧 Run Ledger Patch"):
        st.session_state["patch_done"] = False
        from pymongo import MongoClient
        from config import MONGO_URI
        from fee_calculator import generate_fee_record, SESSION_MONTHS

        client = MongoClient(MONGO_URI)
        db = client["class_mgmt"]
        students = db["students"]
        fee_records = db["fee_records"]

        updated = 0
        for student in students.find({}, {"_id": 0}):
            sid = student["Student ID"]
            fatherless = student.get("Fatherless", False)
            existing_months = {r["month"] for r in fee_records.find({"student_id": sid})}
            missing_months = [m for m in SESSION_MONTHS if m not in existing_months]

            if missing_months:
                full_ledger = generate_fee_record(sid, fatherless)
                patch_docs = [r for r in full_ledger if r["month"] in missing_months]
                fee_records.insert_many(patch_docs)
                updated += 1

        if updated:
            st.success(f"✅ Patched fee records for {updated} students.")
        else:
            st.info("All students already have complete fee ledgers.")
        st.session_state["patch_done"] = True
        
        from pymongo import MongoClient
from config import MONGO_URI
from communication import send_email_receipt, send_sms
import streamlit as st
import os

def communication_controls():
    st.subheader("📬 Guardian Communication Center")

    # MongoDB setup
    client = MongoClient(MONGO_URI)
    db = client["class_mgmt"]
    students = db["students"]

    # Fetch student list
    student_map = {
        f"{s['Student ID']} – {s['Name']}": s
        for s in students.find({}, {"_id": 0, "Student ID": 1, "Name": 1, "Guardian Email": 1, "Mobile": 1})
    }

    # Select student
    selected = st.selectbox("Select Student", list(student_map.keys()))
    student = student_map[selected]
    student_id = student["Student ID"]
    email = student.get("Guardian Email", "")
    phone = student.get("Mobile", "")

    # Select month
    month = st.selectbox("Fee Month", [
        "April", "May", "June", "July", "August", "September",
        "October", "November", "December", "January", "February", "March"
    ])

    # Generate receipt path
    receipt_file = f"receipts/FEE2025-{student_id}-{month}.pdf"

    # Message preview editors
    email_subject = f"Fee Receipt for {month}"
    email_body = st.text_area("Email Message Preview", f"Dear Guardian,\n\nAttached is your official fee receipt for {month}.\n\nBest regards,\nSchool Admin")

    sms_message = st.text_area("SMS Message Preview", f"Dear Guardian, fee for {month} has been received. Ref: FEE2025-{student_id}-{month}.")

    # Unified dispatch toggle
    send_both = st.checkbox("📦 Send Both Email and SMS")

    # Buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📧 Send Email"):
            if os.path.exists(receipt_file):
                sent = send_email_receipt(email, email_subject, email_body, receipt_file)
                st.success("✅ Email sent." if sent else "❌ Failed to send email.")
            else:
                st.warning("⚠️ Receipt file not found.")

    with col2:
        if st.button("📱 Send SMS"):
            success = send_sms(phone, sms_message)
            st.success("✅ SMS sent." if success else "❌ SMS failed.")

    # Unified dispatch
    if send_both and st.button("🚀 Send Both"):
        sms_success = send_sms(phone, sms_message)
        email_success = False
        if os.path.exists(receipt_file):
            email_success = send_email_receipt(email, email_subject, email_body, receipt_file)

        # Results
        if email_success and sms_success:
            st.success("✅ Both Email and SMS sent successfully.")
        elif not email_success and not sms_success:
            st.error("❌ Both dispatches failed.")
        else:
            if email_success:
                st.warning("✅ Email sent, ❌ SMS failed.")
            else:
                st.warning("✅ SMS sent, ❌ Email failed.")


# def communication_controls():
#     st.subheader("📤 Send Communication")

#     student_id = st.text_input("Student ID")
#     month = st.selectbox("Fee Month", [
#         "April", "May", "June", "July", "August", "September",
#         "October", "November", "December", "January", "February", "March"
#     ])
#     email = st.text_input("Guardian's Email")
#     phone = st.text_input("Mobile Number")

#     receipt_file = f"receipts/FEE2025-{student_id}-{month}.pdf"
#     subject = f"Fee Receipt for {month}"
#     body = f"Attached is your official fee receipt for {month}."

#     if st.button("📧 Send Email Receipt"):
#         if os.path.exists(receipt_file):
#             sent = send_email_receipt(email, subject, body, receipt_file)
#             st.success("✅ Email sent successfully." if sent else "❌ Failed to send email.")
#         else:
#             st.warning("Receipt file not found.")

#     if st.button("📱 Send SMS Reminder"):
#         msg = f"Dear Guardian, your child's fee for {month} has been received. Receipt ID: FEE2025-{student_id}-{month}."
#         success = send_sms(phone, msg)
#         st.success("✅ SMS sent." if success else "❌ SMS failed to send.")
