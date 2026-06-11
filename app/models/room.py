from pydantic import BaseModel
from typing import List, Optional

class TimeSlot(BaseModel):
    start_time: str  # Format: "09:00"
    end_time: str    # Format: "11:00"

class Room(BaseModel):
    id: int
    name: str
    capacity: int
    time_slots: List[TimeSlot]  # Доступные слоты для бронирования

class RoomCreate(BaseModel):
    name: str
    capacity: int
    time_slots: List[TimeSlot]

class RoomResponse(BaseModel):
    id: int
    name: str
    capacity: int