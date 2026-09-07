from ast import List
import token

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer , HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.database import get_db
from app.user.model import User
from app.user.repository import UserRepository
from app.user.roles import UserRole


security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:

    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 1. Decode the token using your existing function
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    # 2. Extract user identifier (assuming 'sub' holds the user ID or email)
    user_id_str: str = payload.get("sub")
    if user_id_str is None:
        raise credentials_exception

    #So user_id in jwt paylode is a string but in database it is an integer so we need to convert it to integer
    try:
        user_id = int(user_id_str)
    except ValueError:
        raise credentials_exception

    

    repo = UserRepository(db)
    user = repo.get_by_id(user_id)

    if user is None:
        raise credentials_exception

    return user



def require_user_access(
    current_user: User,
    user_id: int,
) -> None:
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to access this user.",
        )


class RoleChecker:
    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)) -> User:
        if user.role not in [role.value for role in self.allowed_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action error from dependencies.py",
            )
        return user