from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# Base schema for Item
class ItemBase(BaseModel):
    name: str
    email: EmailStr
    item_name: str
    quantity: int
    expiry_date: datetime

# Schema for creating an item
class ItemCreate(ItemBase):
    pass

# Schema for updating an item (insert_date is excluded)
class ItemUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    item_name: Optional[str] = None
    quantity: Optional[int] = None
    expiry_date: Optional[datetime] = None

# Schema for response including insert_date
class ItemResponse(ItemBase):
    id: Optional[str] = None
    insert_date: datetime

class ItemFilter(BaseModel):
    email: Optional[EmailStr] = None  # Use EmailStr for email validation
    expiry_date: Optional[datetime] = None
    insert_date: Optional[datetime] = None
    quantity: Optional[int] = Field(default=None, gt=0)

### clockin Schemas

class ClockInBase(BaseModel):
    email: EmailStr
    location: str

class ClockInCreate(ClockInBase):
    pass

class ClockInResponse(ClockInBase):
    id: str  # Consider using a more descriptive name like `_id` or `clockin_id`
    insert_datetime: datetime

class ClockInUpdate(BaseModel):
    email: Optional[EmailStr] = None
    location: Optional[str] = None

class ClockInFilter(BaseModel):
    email: Optional[EmailStr] = None  # Use EmailStr for email validation
    location: Optional[str] = None