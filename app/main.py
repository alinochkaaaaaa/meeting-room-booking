from fastapi import FastAPI
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
