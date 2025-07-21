from pymongo import MongoClient
from config import MONGO_URI
from fee_calculator import SESSION_MONTHS

client = MongoClient(MONGO_URI)
db = client["class_mgmt"]
students = db["students"]
fee_records = db["fee_records"]

REQUIRED_STUDENT_FIELDS = [
    "R.No", "Student ID", "Name", "FatherName", "MotherName",
    "DOB", "Gender", "Class", "Section", "ContactNo", "Fatherless"
]

def validate_student_schema():
    print("🔍 Validating student documents...")
    all_students = students.find()
    missing_fields_report = []
    for student in all_students:
        missing = [field for field in REQUIRED_STUDENT_FIELDS if field not in student]
        if missing:
            missing_fields_report.append({
                "Student ID": student.get("Student ID", "Unknown"),
                "Missing Fields": missing
            })

    if missing_fields_report:
        print("❗ Students with missing fields:")
        for entry in missing_fields_report:
            print(f"- ID {entry['Student ID']}: Missing {entry['Missing Fields']}")
    else:
        print("✅ All students have complete schema.")

def validate_fee_records():
    print("\n📊 Validating fee records...")
    all_students = students.find()
    issues_found = []

    for student in all_students:
        sid = student["Student ID"]
        fee_docs = list(fee_records.find({"student_id": sid}))
        if len(fee_docs) != 12:
            issues_found.append(f"Student ID {sid} has {len(fee_docs)} fee records (expected 12).")

        # Check month consistency
        recorded_months = {doc["month"] for doc in fee_docs}
        missing_months = set(SESSION_MONTHS) - recorded_months
        if missing_months:
            issues_found.append(f"Student ID {sid} is missing months: {sorted(list(missing_months))}")

    if issues_found:
        print("❗ Fee record issues found:")
        for issue in issues_found:
            print(f"- {issue}")
    else:
        print("✅ All students have complete fee records for April–March.")

if __name__ == "__main__":
    validate_student_schema()
    validate_fee_records()
