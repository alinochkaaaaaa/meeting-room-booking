# Meeting Room Booking Service

Сервис для автоматизации бронирования переговорных комнат в коворкинге.

## Описание

Система позволяет сотрудникам просматривать доступность комнат, создавать и отменять бронирования. Администраторы имеют расширенные права для управления всеми бронированиями.

### Функциональность

- **Аутентификация** через JWT токены
- **Сотрудники**:
  - Просмотр всех комнат
  - Создание бронирований
  - Отмена своих бронирований
- **Администраторы** (дополнительно):
  - Просмотр всех пользователей
  - Просмотр всех бронирований
  - Отмена любых бронирований

### Технологии

- Python 3.13
- FastAPI
- JWT аутентификация
- Poetry (управление зависимостями)
- Pytest (тестирование)
- Docker

## Установка и запуск

### Локальный запуск

#### 1. Клонирование репозитория

```bash
git clone https://github.com/alinochkaaaaaa/meeting-room-booking.git
cd meeting-room-booking
```

#### 2. Установка Poetry

```bash
# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```
```bash
# Linux/Mac
curl -sSL https://install.python-poetry.org | python3 -
```
#### 3. Установка зависимостей
```bash
poetry install
```
#### 4. Запуск сервера
```bash
poetry run uvicorn app.main:app --reload --port 8000
```
Сервер будет доступен по адресу: http://localhost:8000

#### 5. Документация API
Swagger UI: http://localhost:8000/docs

### Запуск в Docker

#### 1. Сборка образа
```bash
docker build -t meeting-room-booking .
```
#### 2. Запуск контейнера
```bash
docker run -p 8000:8000 meeting-room-booking
```
## Примеры работы с API

### 1. Регистрация пользователя
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepass123",
    "role": "employee"
  }'
```
Ответ:
```
json
{
  "id": 1,
  "username": "john_doe",
  "role": "employee"
}
```
### 2. Вход в систему (получение токена)
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -d "username=john_doe&password=securepass123"
```
Ответ:
```
json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user_id": 1,
  "role": "employee"
}
```
### 3. Получение списка комнат
```bash
curl -X GET "http://localhost:8000/api/v1/rooms" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
Ответ:
```
json
[
  {
    "id": 1,
    "name": "Meeting Room A",
    "capacity": 8
  },
  {
    "id": 2,
    "name": "Meeting Room B",
    "capacity": 4
  }
]
```
### 4. Создание бронирования
```bash
curl -X POST "http://localhost:8000/api/v1/bookings" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "room_id": 1,
    "booking_date": "2026-06-15",
    "time_slot_start": "09:00",
    "time_slot_end": "11:00"
  }'
```
Ответ:
```
json
{
  "id": 1,
  "room_id": 1,
  "room_name": "Meeting Room A",
  "booking_date": "2026-06-15",
  "time_slot_start": "09:00",
  "time_slot_end": "11:00",
  "status": "active"
}
```
### 5. Просмотр своих бронирований
```bash
curl -X GET "http://localhost:8000/api/v1/bookings" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
### 6. Отмена бронирования
```bash
curl -X DELETE "http://localhost:8000/api/v1/bookings/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
Ответ:
```
json
{
  "message": "Booking cancelled successfully"
}
```

### 7. Администратор: просмотр всех пользователей
```bash
curl -X GET "http://localhost:8000/api/v1/admin/users" \
  -H "Authorization: Bearer ADMIN_TOKEN"
```
### 8. Администратор: просмотр всех бронирований
```bash
curl -X GET "http://localhost:8000/api/v1/admin/bookings" \
  -H "Authorization: Bearer ADMIN_TOKEN"
```
### 9. Администратор: отмена любого бронирования
```bash
curl -X DELETE "http://localhost:8000/api/v1/admin/bookings/1" \
  -H "Authorization: Bearer ADMIN_TOKEN"
```
## Тестовые данные
При первом запуске автоматически создаются:
```
Администратор: admin / admin123

Комнаты:
Meeting Room A (вместимость: 8 человек)
Meeting Room B (вместимость: 4 человека)
```
## Структура проекта
```
meeting-room-booking/

├── app/
│   ├── api/              # Эндпоинты API
│   ├── core/             # Конфигурация и безопасность
│   ├── models/           # Pydantic модели
│   ├── repositories/     # Работа с данными
│   ├── services/         # Бизнес-логика
│   └── main.py           # Точка входа
├── tests/                # Юнит-тесты
├── Dockerfile            # Docker конфигурация
├── pyproject.toml        # Зависимости Poetry
└── README.md
```
## API Endpoints
```
Метод	Эндпоинт	                Описание	               Доступ
POST	/api/v1/auth/register	        Регистрация	               Все
POST	/api/v1/auth/login	        Вход (JWT)	               Все
GET	/api/v1/rooms	                Список комнат	               Сотрудник+
POST	/api/v1/rooms	                Создание комнаты	       Админ
GET	/api/v1/bookings	        Мои бронирования	       Сотрудник+
POST	/api/v1/bookings	        Создание бронирования	       Сотрудник+
DELETE	/api/v1/bookings/{id}	        Отмена бронирования	       Сотрудник+
GET	/api/v1/admin/users	        Все пользователи	       Админ
GET  	/api/v1/admin/bookings	        Все бронирования	       Админ
DELETE	/api/v1/admin/bookings/{id}	Отмена бронирования            Админ
```

## Запуск тестов

```bash
poetry run pytest tests/ -v
```