from fastapi import APIRouter, Depends, HTTPException, status
from app.repositories.booking_repo import BookingRepository
from app.repositories.user_repo import UserRepository
from app.repositories.room_repo import RoomRepository
from app.api.dependencies import get_current_admin
from app.models.user import User, UserResponse
from app.models.booking import BookingResponse
from app.models.room import Room, RoomResponse

router = APIRouter()


@router.get("/users", response_model=list[UserResponse])
def get_all_users(current_user: User = Depends(get_current_admin)):
    users = UserRepository.get_all_users()
    return [UserResponse(id=u.id, username=u.username, role=u.role) for u in users]


@router.get("/bookings", response_model=list[BookingResponse])
def get_all_bookings(current_user: User = Depends(get_current_admin)):
    bookings = BookingRepository.get_all_bookings()
    result = []
    for booking in bookings:
        room = RoomRepository.get_room(booking.room_id)
        room_name = room.name if room else "Unknown"
        result.append(BookingResponse(
            id=booking.id,
            room_id=booking.room_id,
            room_name=room_name,
            booking_date=booking.booking_date,
            time_slot_start=booking.time_slot_start,
            time_slot_end=booking.time_slot_end,
            status=booking.status.value
        ))
    return result


@router.delete("/bookings/{booking_id}")
def admin_cancel_booking(booking_id: int, current_user: User = Depends(get_current_admin)):
    success = BookingRepository.cancel_booking(booking_id, current_user.id, is_admin=True)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    return {"message": "Booking cancelled by admin"}