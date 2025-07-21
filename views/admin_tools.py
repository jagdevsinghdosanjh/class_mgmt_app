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

def communication_controls():
    st.subheader("📤 Send Communication")

    student_id = st.text_input("Student ID")
    month = st.selectbox("Fee Month", [
        "April", "May", "June", "July", "August", "September",
        "October", "November", "December", "January", "February", "March"
    ])
    email = st.text_input("Guardian's Email")
    phone = st.text_input("Mobile Number")

    receipt_file = f"receipts/FEE2025-{student_id}-{month}.pdf"
    subject = f"Fee Receipt for {month}"
    body = f"Attached is your official fee receipt for {month}."

    if st.button("📧 Send Email Receipt"):
        if os.path.exists(receipt_file):
            sent = send_email_receipt(email, subject, body, receipt_file)
            st.success("✅ Email sent successfully." if sent else "❌ Failed to send email.")
        else:
            st.warning("Receipt file not found.")

    if st.button("📱 Send SMS Reminder"):
        msg = f"Dear Guardian, your child's fee for {month} has been received. Receipt ID: FEE2025-{student_id}-{month}."
        success = send_sms(phone, msg)
        st.success("✅ SMS sent." if success else "❌ SMS failed to send.")
