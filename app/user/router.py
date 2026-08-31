from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.user.model import User
from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.user.repository import UserRepository
from app.user.schema import (
    MessageResponse,
    PasswordChange,
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate,
    TokenResponse,
)
from app.user.service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repo = UserRepository(db)
    return UserService(repo)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def register_user(
    payload: UserCreate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    return service.register_user(payload)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Verify user credentials and login",
)
def login_user(
    payload: UserLogin,
    service: UserService = Depends(get_user_service),
) -> TokenResponse:
    access_token = service.login_user(payload)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get user profile by ID",
)
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    return service.get_user_by_id(user_id, current_user)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Update user profile",
)
def update_user(
    user_id: int,
    payload: UserUpdate,
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    return service.update_user(user_id, payload, current_user)


@router.post(
    "/{user_id}/change-password",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Change user password",
)
def change_password(
    user_id: int,
    payload: PasswordChange,
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
) -> dict[str, str]:
    return service.change_password(user_id, payload ,current_user)