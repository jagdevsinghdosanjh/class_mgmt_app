import streamlit as st
from database import fetch_all_students, find_students_by_field, get_birthdays_by_month
from datetime import datetime

def format_student_card(student):
    st.markdown(f"""
    **{student['Name']}** ({student['Gender']})  
    📚 Roll No: {student['R.No']}, Class {student['Class']} - {student['Section']}  
    👨 {student['FatherName']} | 👩 {student['MotherName']}  
    🎂 DOB: {student['DOB']}  
    📞 Contact: `{student['ContactNo']}`  
    """)

def student_dashboard():
    st.title("📋 Student Dashboard")

    students = fetch_all_students()
    search_name = st.text_input("🔍 Search by Name")
    gender_filter = st.selectbox("Filter by Gender", ["All", "Male", "Female"])
    dob_filter = st.selectbox("🎂 Birthday Month", ["All"] + [f"{m:02}" for m in range(1, 13)])

    filtered = students

    if search_name:
        filtered = find_students_by_field("Name", search_name)

    if gender_filter != "All":
        filtered = [s for s in filtered if s.get("Gender", "").lower() == gender_filter.lower()]

    if dob_filter != "All":
        filtered = [s for s in filtered if f"-{dob_filter}-" in s.get("DOB", "")]

    st.subheader(f"Showing {len(filtered)} students")
    for student in filtered:
        format_student_card(student)
        st.markdown("---")

    if st.button("Show Birthday Summary"):
        month_today = datetime.now().strftime("%m")
        bday_students = get_birthdays_by_month(month_today)
        st.success(f"{len(bday_students)} students have birthdays this month 🎉")

