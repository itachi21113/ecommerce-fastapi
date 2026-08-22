from fastapi import HTTPException, status
from app.core.security import hash_password
from app.user.model import User
from app.user.repository import UserRepository
from app.user.schema import UserCreate


class UserService:

    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    def register_user(self, payload: UserCreate) -> User:
        # Step 1: Check if user already exists
        existing_user = self.repo.get_by_email(email=payload.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists.",
            )

        # Step 2: Hash plain text password
        hashed_pwd = hash_password(payload.password)

        # Step 3: Instantiate model
        new_user = User(
            name=payload.name,
            email=payload.email,
            hashed_password=hashed_pwd,
        )

        # Step 4: Persist via repository
        return self.repo.create(new_user)