from configuration import items_collection, clockins_collection
from datetime import datetime
from bson import ObjectId
from typing import List, Optional
from database.schemas import ClockInCreate, ClockInUpdate

# Helper to convert MongoDB document to Python dict
def item_helper(item: dict) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "email": item["email"],
        "item_name": item["item_name"],
        "quantity": item["quantity"],
        "expiry_date": item["expiry_date"].strftime("%Y-%m-%d"),
        "insert_date": item["insert_date"].strftime("%Y-%m-%d"),
    }

# CRUD operations for Items
def create_item(item_data: dict) -> dict:
    item_data['insert_date'] = datetime.utcnow()
    result = items_collection.insert_one(item_data)
    return item_helper(items_collection.find_one({"_id": result.inserted_id}))

def get_all_items() -> list:
    items = items_collection.find()
    return [item_helper(item) for item in items]

def get_item(id: str) -> dict:
    item = items_collection.find_one({"_id": ObjectId(id)})
    if item:
        return item_helper(item)
    return None

def update_item(id: str, update_data: dict) -> dict:
    items_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    return item_helper(items_collection.find_one({"_id": ObjectId(id)}))

def delete_item(id: str) -> bool:
    result = items_collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0


def create_clock_in(clockin_data: ClockInCreate):
    clockin_data = clockin_data.dict()
    clockin_data["insert_datetime"] = datetime.utcnow()  # Automatically set the Insert DateTime
    result = clockins_collection.insert_one(clockin_data)
    return get_clock_in(str(result.inserted_id))

def get_clock_in(clockin_id: str):
    clockin = clockins_collection.find_one({"_id": ObjectId(clockin_id)})
    return object_id_to_str(clockin)

def get_all_clock_ins():
    clockins = list(clockins_collection.find())
    return [object_id_to_str(clockin) for clockin in clockins]

def update_clock_in(clockin_id: str, clockin_data: ClockInUpdate):
    update_data = {k: v for k, v in clockin_data.items() if v is not None}
    if update_data:
        clockins_collection.update_one({"_id": ObjectId(clockin_id)}, {"$set": update_data})
    return get_clock_in(clockin_id)

def delete_clock_in(clockin_id: str):
    result = clockins_collection.delete_one({"_id": ObjectId(clockin_id)})
    return result.deleted_count > 0

def object_id_to_str(item):
    if "_id" in item:
        item["id"] = str(item.pop("_id"))
    return item
