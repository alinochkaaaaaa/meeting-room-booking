# fix_encoding.py
import os
import shutil

# Содержимое всех файлов в правильной кодировке (UTF-8)
# !!! ВАЖНО: Убедитесь, что этот файл (fix_encoding.py) сохранён в PyCharm в кодировке UTF-8 !!!

FILES = {
    # app/main.py
    "app/main.py": '''from fastapi import FastAPI
from app.api.v1.endpoints import auth, rooms, bookings, admin

app = FastAPI(title="Meeting Room Booking")

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(rooms.router, prefix="/api/v1/rooms", tags=["rooms"])
app.include_router(bookings.router, prefix="/api/v1/bookings", tags=["bookings"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])

@app.get("/")
def root():
    return {"message": "Meeting Room Booking API"}

@app.on_event("startup")
def startup():
    from app.repositories.user_repo import UserRepository
    from app.core.security import get_password_hash
    from app.models.user import UserRole

    admin = UserRepository.get_user_by_username("admin")
    if not admin:
        hashed_pw = get_password_hash("admin123")
        UserRepository.create_user("admin", hashed_pw, UserRole.ADMIN)
        print("Test admin created: username='admin', password='admin123'")

    from app.repositories.room_repo import RoomRepository
    from app.models.room import TimeSlot

    rooms = RoomRepository.get_all_rooms()
    if not rooms:
        time_slots = [
            TimeSlot(start_time="09:00", end_time="11:00"),
            TimeSlot(start_time="11:00", end_time="13:00"),
            TimeSlot(start_time="13:00", end_time="15:00"),
            TimeSlot(start_time="15:00", end_time="17:00"),
            TimeSlot(start_time="17:00", end_time="19:00")
        ]
        RoomRepository.create_room("Meeting Room A", 8, time_slots)
        RoomRepository.create_room("Meeting Room B", 4, time_slots)
        print("Test rooms created")
''',

    # app/models/booking.py
    "app/models/booking.py": '''from enum import Enum
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
    time_slot_start: str
    time_slot_end: str
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
''',
}

# Функция для перезаписи всех файлов в нужной кодировке
def rewrite_files():
    # Сначала удалим старые файлы, которые могут быть повреждены
    for filepath in FILES.keys():
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"Removed old file: {filepath}")

    # Запишем новые файлы в кодировке UTF-8
    for filepath, content in FILES.items():
        # Убедимся, что директория существует
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Rewritten: {filepath}")

if __name__ == "__main__":
    rewrite_files()
    print("\\nDone! Now try running: poetry run uvicorn app.main:app --reload")