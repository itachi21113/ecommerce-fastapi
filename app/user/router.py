from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.user.repository import UserRepository
from app.user.schema import UserCreate, UserResponse
from app.user.service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Dependency injection to assemble UserRepository and UserService."""
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
    """Accept name, email, and password in JSON body to create a new user account."""
    return service.register_user(payload)