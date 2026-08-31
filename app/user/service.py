from fastapi import HTTPException, status

from app.core.security import hash_password, verify_password , create_access_token
from app.user.model import User
from app.user.repository import UserRepository
from app.user.schema import PasswordChange, UserCreate, UserLogin, UserUpdate


class UserService:

    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    def register_user(self, payload: UserCreate) -> User:
        existing_user = self.repo.get_by_email(email=payload.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists.",
            )

        hashed_pwd = hash_password(payload.password)
        new_user = User(
            name=payload.name,
            email=payload.email,
            hashed_password=hashed_pwd,
        )
        return self.repo.create(new_user)

    def login_user(self, payload: UserLogin) -> str:
        user = self.repo.get_by_email(email=payload.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        is_valid = verify_password(payload.password, user.hashed_password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        return create_access_token(user.id)

    def get_user_by_id(self, user_id: int) -> User:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found.",
            )
        return user

    def update_user(self, user_id: int, payload: UserUpdate) -> User:
        user = self.get_user_by_id(user_id)

        if payload.name is not None:
            user.name = payload.name

        return self.repo.save(user)

    def change_password(
        self, user_id: int, payload: PasswordChange
    ) -> dict[str, str]:
        user = self.get_user_by_id(user_id)

        # 1. Check old password
        if not verify_password(payload.old_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password does not match.",
            )

        # 2. Hash and save new password
        user.hashed_password = hash_password(payload.new_password)
        self.repo.save(user)

        return {"message": "Password updated successfully."}