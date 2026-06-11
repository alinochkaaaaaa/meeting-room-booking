from fastapi import APIRouter, Depends, HTTPException, status
from app.repositories.booking_repo import BookingRepository
from app.repositories.room_repo import RoomRepository
from app.models.booking import BookingCreate, BookingResponse
from app.api.dependencies import get_current_user
from app.models.user import User, UserRole
from datetime import datetime

router = APIRouter()


@router.get("/", response_model=list[BookingResponse])
def get_my_bookings(current_user: User = Depends(get_current_user)):
    bookings = BookingRepository.get_user_bookings(current_user.id)
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


@router.post("/", response_model=BookingResponse)
def create_booking(booking_data: BookingCreate, current_user: User = Depends(get_current_user)):
    # Проверяем, существует ли комната
    room = RoomRepository.get_room(booking_data.room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    # Проверяем, не занят ли слот
    if BookingRepository.check_conflict(booking_data.room_id, booking_data.booking_date, booking_data.time_slot_start):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Time slot already booked")

    # Создаём бронирование
    booking = BookingRepository.create_booking(
        room_id=booking_data.room_id,
        user_id=current_user.id,
        booking_date=booking_data.booking_date,
        time_slot_start=booking_data.time_slot_start,
        time_slot_end=booking_data.time_slot_end
    )

    return BookingResponse(
        id=booking.id,
        room_id=booking.room_id,
        room_name=room.name,
        booking_date=booking.booking_date,
        time_slot_start=booking.time_slot_start,
        time_slot_end=booking.time_slot_end,
        status=booking.status.value
    )


@router.delete("/{booking_id}")
def cancel_booking(booking_id: int, current_user: User = Depends(get_current_user)):
    success = BookingRepository.cancel_booking(booking_id, current_user.id, is_admin=False)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found or cannot be cancelled")

    return {"message": "Booking cancelled successfully"}