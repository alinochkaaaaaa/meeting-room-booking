from app.models.room import Room, TimeSlot
from typing import Dict, List, Optional

# Фейковая БД комнат
rooms_db: Dict[int, Room] = {}
next_room_id = 1


class RoomRepository:

    @staticmethod
    def create_room(name: str, capacity: int, time_slots: List[TimeSlot]) -> Room:
        global next_room_id
        room = Room(
            id=next_room_id,
            name=name,
            capacity=capacity,
            time_slots=time_slots
        )
        rooms_db[next_room_id] = room
        next_room_id += 1
        return room

    @staticmethod
    def get_room(room_id: int) -> Optional[Room]:
        return rooms_db.get(room_id)

    @staticmethod
    def get_all_rooms() -> List[Room]:
        return list(rooms_db.values())

    @staticmethod
    def delete_room(room_id: int) -> bool:
        if room_id in rooms_db:
            del rooms_db[room_id]
            return True
        return False