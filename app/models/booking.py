from enum import Enum
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class BookingStatus(str, Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"

class Booking(BaseModel):
    id: int
    room_id: int
    user_id: int
    booking_date: date
    time_slot_start: str  # Format: "09:00"
    time_slot_end: str    # Format: "11:00"
    status: BookingStatus = BookingStatus.ACTIVE
    created_at: datetime
    cancelled_at: Optional[datetime] = None

class BookingCreate(BaseModel):
    room_id: int
    booking_date: date
    time_slot_start: str
    time_slot_end: str

class BookingResponse(BaseModel):
    id: int
    room_id: int
    room_name: str
    booking_date: date
    time_slot_start: str
    time_slot_end: str
    status: str