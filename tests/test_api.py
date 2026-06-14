import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.repositories.room_repo import RoomRepository
from app.repositories.user_repo import UserRepository
from app.models.room import TimeSlot
from app.models.user import UserRole
from app.core.security import get_password_hash

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def setup_test_data():
    """Создаём тестовые данные перед запуском всех тестов"""
    # Создаём админа
    admin = UserRepository.get_user_by_username("admin")
    if not admin:
        hashed_pw = get_password_hash("admin123")
        UserRepository.create_user("admin", hashed_pw, UserRole.ADMIN)

    # Создаём комнаты
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

    yield


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Meeting Room Booking API"}


def test_register_user():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser2",
            "password": "test123",
            "role": "employee"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser2"
    assert data["role"] == "employee"
    assert "id" in data


def test_register_existing_user():
    # Сначала создаём пользователя
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "duplicate",
            "password": "test123",
            "role": "employee"
        }
    )
    # Пробуем создать с тем же именем
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "duplicate",
            "password": "test123",
            "role": "employee"
        }
    )
    assert response.status_code == 400
    assert "Username already exists" in response.text


def test_login():
    # Сначала создаём пользователя
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "loginuser",
            "password": "loginpass",
            "role": "employee"
        }
    )

    # Логинимся
    response = client.post(
        "/api/v1/auth/login",
        params={"username": "loginuser", "password": "loginpass"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["role"] == "employee"


def test_login_invalid():
    response = client.post(
        "/api/v1/auth/login",
        params={"username": "nonexistent", "password": "wrong"}
    )
    assert response.status_code == 401
    assert "Invalid credentials" in response.text


def test_get_rooms_unauthorized():
    # Без токена должен вернуть 401
    response = client.get("/api/v1/rooms")
    assert response.status_code == 401


def test_get_rooms_authorized():
    # Создаём пользователя и получаем токен
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "roomuser",
            "password": "roompass",
            "role": "employee"
        }
    )
    login_response = client.post(
        "/api/v1/auth/login",
        params={"username": "roomuser", "password": "roompass"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Запрашиваем комнаты с токеном
    response = client.get(
        "/api/v1/rooms",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    rooms = response.json()
    assert isinstance(rooms, list)
    assert len(rooms) > 0  # Должны быть комнаты
    assert "id" in rooms[0]
    assert "name" in rooms[0]
    assert "capacity" in rooms[0]


def test_create_booking():
    # Создаём пользователя
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "bookinguser",
            "password": "bookingpass",
            "role": "employee"
        }
    )
    assert register_response.status_code == 200

    login_response = client.post(
        "/api/v1/auth/login",
        params={"username": "bookinguser", "password": "bookingpass"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Создаём бронирование
    response = client.post(
        "/api/v1/bookings",
        json={
            "room_id": 1,
            "booking_date": "2026-12-31",
            "time_slot_start": "09:00",
            "time_slot_end": "11:00"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["room_id"] == 1
    assert data["status"] == "active"


def test_admin_access():
    # Логинимся как admin
    login_response = client.post(
        "/api/v1/auth/login",
        params={"username": "admin", "password": "admin123"}
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # Админ может получить список пользователей
    response = client.get(
        "/api/v1/admin/users",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) > 0


def test_get_all_bookings_admin():
    # Логинимся как admin
    login_response = client.post(
        "/api/v1/auth/login",
        params={"username": "admin", "password": "admin123"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Админ может получить все бронирования
    response = client.get(
        "/api/v1/admin/bookings",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    bookings = response.json()
    assert isinstance(bookings, list)