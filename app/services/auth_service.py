from app.repositories.user_repo import UserRepository
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.user import UserRole, UserResponse
from datetime import timedelta
from app.core.config import settings


class AuthService:

    @staticmethod
    def register_user(username: str, password: str, role: UserRole = UserRole.EMPLOYEE):
        # Проверяем, существует ли пользователь
        existing_user = UserRepository.get_user_by_username(username)
        if existing_user:
            return None, "Username already exists"

        # Создаём пользователя
        hashed_password = get_password_hash(password)
        user = UserRepository.create_user(username, hashed_password, role)

        return UserResponse(id=user.id, username=user.username, role=user.role), None

    @staticmethod
    def login_user(username: str, password: str):
        user = UserRepository.get_user_by_username(username)
        if not user:
            return None, "Invalid credentials"

        if not verify_password(password, user.hashed_password):
            return None, "Invalid credentials"

        # Создаём JWT токен
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "user_id": user.id, "role": user.role.value},
            expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer", "user_id": user.id, "role": user.role.value}, None