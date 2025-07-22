import streamlit as st
from datetime import datetime
from database import students_collection
from fee_calculator import generate_fee_record

# MongoDB collection for fee records
fee_collection = students_collection.database["fee_records"]

def create_fee_ledger(student):
    student_id = student["Student ID"]
    fatherless = student.get("Fatherless", False)
    ledger = generate_fee_record(student_id, fatherless)
    fee_collection.insert_many(ledger)

def fetch_fee_records(student_id):
    return list(fee_collection.find({"student_id": student_id}, {"_id": 0}))

def fee_view():
    st.title("💰 Fee Ledger Viewer")

    # Load all students
    students = students_collection.find({}, {"_id": 0})
    student_names = [s["Name"] for s in students]
    selected_name = st.selectbox("Select Student", student_names)

    student = next((s for s in students if s["Name"] == selected_name), None)
    if not student:
        st.warning("Student not found.")
        return

    # Auto-generate ledger if missing
    student_id = student["Student ID"]
    existing = fee_collection.count_documents({"student_id": student_id})
    if existing == 0:
        create_fee_ledger(student)

    records = fetch_fee_records(student_id)

    st.subheader(f"Fee Ledger for {student['Name']}")
    for record in records:
        status = "✅ Paid" if record["paid"] else "❌ Unpaid"
        st.markdown(f"- {record['month']} {record['year']}: ₹{record['fee_due']} {status}")

    # Mark months as paid (optional)
    unpaid_months = [r for r in records if not r["paid"]]
    if unpaid_months:
        unpaid_labels = [f"{r['month']} {r['year']}" for r in unpaid_months]
        selected = st.multiselect("Mark Paid Months", unpaid_labels)

        if st.button("Update Payment Status"):
            for r in unpaid_months:
                label = f"{r['month']} {r['year']}"
                if label in selected:
                    fee_collection.update_one(
                        {"student_id": student_id, "month": r["month"], "year": r["year"]},
                        {"$set": {"paid": True}}
                    )
            st.success("Updated payment status!")

