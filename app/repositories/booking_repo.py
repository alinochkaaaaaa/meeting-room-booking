from app.models.booking import Booking, BookingStatus
from datetime import datetime
from typing import Dict, List, Optional

# Фейковая БД бронирований
bookings_db: Dict[int, Booking] = {}
next_booking_id = 1


class BookingRepository:

    @staticmethod
    def create_booking(room_id: int, user_id: int, booking_date, time_slot_start: str, time_slot_end: str) -> Booking:
        global next_booking_id
        booking = Booking(
            id=next_booking_id,
            room_id=room_id,
            user_id=user_id,
            booking_date=booking_date,
            time_slot_start=time_slot_start,
            time_slot_end=time_slot_end,
            status=BookingStatus.ACTIVE,
            created_at=datetime.now()
        )
        bookings_db[next_booking_id] = booking
        next_booking_id += 1
        return booking

    @staticmethod
    def get_booking(booking_id: int) -> Optional[Booking]:
        return bookings_db.get(booking_id)

    @staticmethod
    def get_user_bookings(user_id: int) -> List[Booking]:
        return [b for b in bookings_db.values() if b.user_id == user_id and b.status == BookingStatus.ACTIVE]

    @staticmethod
    def get_all_bookings() -> List[Booking]:
        return list(bookings_db.values())

    @staticmethod
    def cancel_booking(booking_id: int, user_id: int, is_admin: bool = False) -> bool:
        booking = bookings_db.get(booking_id)
        if not booking:
            return False

        # Проверка прав: только владелец или админ
        if not is_admin and booking.user_id != user_id:
            return False

        if booking.status == BookingStatus.ACTIVE:
            booking.status = BookingStatus.CANCELLED
            booking.cancelled_at = datetime.now()
            return True
        return False

    @staticmethod
    def check_conflict(room_id: int, booking_date, time_slot_start: str,
                       exclude_booking_id: Optional[int] = None) -> bool:
        for booking in bookings_db.values():
            if booking.room_id == room_id and booking.booking_date == booking_date:
                if booking.status == BookingStatus.ACTIVE:
                    if exclude_booking_id and booking.id == exclude_booking_id:
                        continue
                    if booking.time_slot_start == time_slot_start:
                        return True
        return False