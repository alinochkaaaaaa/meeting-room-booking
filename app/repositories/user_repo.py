from app.models.user import User, UserRole
from typing import Dict, Optional

# Фейковая БД пользователей
users_db: Dict[int, User] = {}
next_user_id = 1


class UserRepository:

    @staticmethod
    def create_user(username: str, hashed_password: str, role: UserRole) -> User:
        global next_user_id
        user = User(
            id=next_user_id,
            username=username,
            hashed_password=hashed_password,
            role=role
        )
        users_db[next_user_id] = user
        next_user_id += 1
        return user

    @staticmethod
    def get_user_by_username(username: str) -> Optional[User]:
        for user in users_db.values():
            if user.username == username:
                return user
        return None

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        return users_db.get(user_id)

    @staticmethod
    def get_all_users() -> list[User]:
        return list(users_db.values())