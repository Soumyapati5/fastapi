from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime
from database import model
from database.schemas import ClockInCreate, ClockInResponse, ClockInUpdate, ClockInFilter
from configuration import clockins_collection
from bson.objectid import ObjectId
from pydantic import EmailStr

router = APIRouter()

@router.post("/", response_model=ClockInResponse)
def create_clock_in(clockin: ClockInCreate):
    return model.create_clock_in(clockin)

@router.get("/{id}", response_model=ClockInResponse)
def get_clock_in(id: str):
    clockin = model.get_clock_in(id)
    if clockin is None:
        raise HTTPException(status_code=404, detail="Clock-in record not found")
    return clockin

@router.put("/{id}", response_model=ClockInResponse)
def update_clock_in(id: str, clockin: ClockInUpdate):
    updated_clockin = model.update_clock_in(id, clockin)
    if not updated_clockin:
        raise HTTPException(status_code=404, detail="Clock-in record not found")
    return updated_clockin

@router.delete("/{id}")
def delete_clock_in(id: str):
    success = model.delete_clock_in(id)
    if not success:
        raise HTTPException(status_code=404, detail="Clock-in record not found")
    return {"message": "Clock-in record deleted successfully"}

@router.get("/clockin/filter", response_model=List[ClockInResponse])
def filter_clock_ins(filter: ClockInFilter = Depends()):
    query = {}
    if filter.email:
        query["email"] = filter.email
    if filter.location:
        query['location'] = filter.location

    items = list(model.clockins_collection.find(query))
    if not items:
        raise HTTPException(status_code=404, detail="No items found with the provided filter")
    return [model.object_id_to_str(item) for item in items]

@router.get("/", response_model=List[ClockInResponse])
def get_all_clock_ins():
    """Retrieve all clock-in records."""
    return model.get_all_clock_ins()
