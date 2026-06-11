from fastapi import APIRouter, Depends, HTTPException, status
from app.repositories.room_repo import RoomRepository
from app.models.room import Room, RoomCreate, RoomResponse
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=list[RoomResponse])
def get_rooms(current_user: User = Depends(get_current_user)):
    rooms = RoomRepository.get_all_rooms()
    return [RoomResponse(id=r.id, name=r.name, capacity=r.capacity) for r in rooms]


@router.post("/", response_model=RoomResponse)
def create_room(room_data: RoomCreate, current_user: User = Depends(get_current_user)):
    # Только админ может создавать комнаты
    from app.models.user import UserRole
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")

    room = RoomRepository.create_room(room_data.name, room_data.capacity, room_data.time_slots)
    return RoomResponse(id=room.id, name=room.name, capacity=room.capacity)