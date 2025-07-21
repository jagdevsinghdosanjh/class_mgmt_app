from pymongo import MongoClient
import pandas as pd
from config import MONGO_URI

# Initialize MongoDB client and database
client = MongoClient(MONGO_URI)
db = client["class_mgmt"]
students_collection = db["students"]

def load_students_from_csv(csv_path="data/student.csv"):
    df = pd.read_csv(csv_path)
    records = df.to_dict(orient="records")
    students_collection.insert_many(records)
    return len(records)

def fetch_all_students():
    return list(students_collection.find({}, {"_id": 0}))

def find_students_by_field(field, value):
    query = {field: {"$regex": value, "$options": "i"}}
    return list(students_collection.find(query, {"_id": 0}))

def get_birthdays_by_month(month_str):
    return list(students_collection.find({"DOB": {"$regex": f"-{month_str}-", "$options": "i"}}, {"_id": 0}))

