from fastapi import APIRouter, HTTPException, Depends
from database import model
from database.schemas import ItemCreate, ItemUpdate, ItemResponse, ItemFilter
from typing import List, Optional
from bson import ObjectId
from pydantic import EmailStr
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=ItemResponse)
def create_item(item: ItemCreate):
    return model.create_item(item.dict())

@router.get("/{id}", response_model=ItemResponse)
def get_item(id: str):
    # Ensure the ID is a valid ObjectId
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    item = model.get_item(id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.get("/", response_model=List[ItemResponse])
def get_all_items():
    items = model.get_all_items()
    if not items:
        raise HTTPException(status_code=404, detail="No items found")
    return items

@router.put("/{id}", response_model=ItemResponse)
def update_item(id: str, item: ItemUpdate):
    updated_item = model.update_item(id, item.dict(exclude_unset=True))
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@router.delete("/{id}")
def delete_item(id: str):
    success = model.delete_item(id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}

@router.get("/items/filter", response_model=List[ItemResponse])
def filter_items(filter: ItemFilter = Depends()):
    query = {}

    if filter.email:
        query["email"] = filter.email
    if filter.expiry_date:
        query["expiry_date"] = {"$gt": filter.expiry_date}  # Greater than
    if filter.insert_date:
        query["insert_date"] = {"$lt": filter.insert_date}  # Less than
    if filter.quantity is not None:
        query["quantity"] = {"$gte": filter.quantity}  # Greater than or equal to

    items = list(model.items_collection.find(query))
    if not items:
        raise HTTPException(status_code=404, detail="No items found with the provided filter")
    return [model.object_id_to_str(item) for item in items]

@router.get("/items/count_by_email")
def count_items_by_email(email: Optional[EmailStr] = None):
    if email:
        # Filter by email if provided
        pipeline = [
            {"$match": {"email": email}},
            {"$group": {"_id": "$email", "count": {"$sum": 1}}}
        ]
    else:
        # Count for all emails
        pipeline = [
            {"$group": {"_id": "$email", "count": {"$sum": 1}}}
        ]

    result = list(model.items_collection.aggregate(pipeline))
    return {"counts": result}