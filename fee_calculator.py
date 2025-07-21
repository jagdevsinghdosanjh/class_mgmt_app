from datetime import datetime

# Fee breakdown for non-fatherless students
FEE_STRUCTURE = {
    "Admission Fee": 0,
    "Tuition Fee": 0,
    "Absentee Fine": 0,
    "Late Fee Fine": 0,
    "Amalgamated Fund": 20,
    "PTA Fund": 15,
    "Sports Fund": 15,
    "Other": 5,
    "Continuation Fee": 200
}

TOTAL_MONTHLY_FEE = sum(FEE_STRUCTURE.values())

# Academic session months
SESSION_MONTHS = [
    'April', 'May', 'June', 'July', 'August', 'September',
    'October', 'November', 'December',
    'January', 'February', 'March'
]

def calculate_monthly_fee(fatherless: bool) -> int:
    return 0 if fatherless else TOTAL_MONTHLY_FEE

def generate_fee_record(student_id: int, fatherless: bool):
    fee_records = []
    for i, month in enumerate(SESSION_MONTHS):
        # Split session year: April–Dec is start year, Jan–March is next year
        year = 2025 if i < 9 else 2026
        fee_due = calculate_monthly_fee(fatherless)

        fee_records.append({
            "student_id": student_id,
            "month": month,
            "year": str(year),
            "fee_due": fee_due,
            "paid": False
        })
    return fee_records

