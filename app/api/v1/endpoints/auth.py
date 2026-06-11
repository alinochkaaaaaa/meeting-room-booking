from fastapi import APIRouter, HTTPException, status
from app.models.user import UserCreate, UserResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate):
    user, error = AuthService.register_user(
        username=user_data.username,
        password=user_data.password,
        role=user_data.role
    )

    if error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return user


@router.post("/login")
def login(username: str, password: str):
    result, error = AuthService.login_user(username, password)

    if error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error)

    return result