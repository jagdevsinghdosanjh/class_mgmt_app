from pymongo import MongoClient
from config import MONGO_URI
from fee_calculator import generate_fee_record, SESSION_MONTHS

client = MongoClient(MONGO_URI)
db = client["class_mgmt"]
students = db["students"]
fee_records = db["fee_records"]

def patch_fee_ledgers():
    print("🧪 Checking and patching fee records...")
    updated_students = []

    for student in students.find({}, {"_id": 0}):
        sid = student["Student ID"]
        fatherless = student.get("Fatherless", False)
        existing_months = {r["month"] for r in fee_records.find({"student_id": sid})}

        missing_months = [m for m in SESSION_MONTHS if m not in existing_months]
        if missing_months:
            print(f"🔧 Student ID {sid} is missing months: {missing_months}")
            full_ledger = generate_fee_record(sid, fatherless)
            patch_docs = [r for r in full_ledger if r["month"] in missing_months]
            fee_records.insert_many(patch_docs)
            updated_students.append(sid)

    if updated_students:
        print(f"\n✅ Patched fee records for {len(updated_students)} students.")
    else:
        print("✅ All students have complete fee ledgers.")

if __name__ == "__main__":
    patch_fee_ledgers()
