from app.user.service import UserService
import pytest
from unittest.mock import MagicMock
from app.user.schema import UserCreate, UserLogin
from fastapi import HTTPException
from app.core.security import hash_password, verify_password

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def db_session():
    return MagicMock()

@pytest.fixture
def mock_refresh_token_service():
    return MagicMock()

@pytest.fixture
def user_service(mock_repo, mock_refresh_token_service, db_session):
    return UserService(
        repo=mock_repo,
        refresh_token_service=mock_refresh_token_service,
        db=db_session,
    )

@pytest.fixture
def mock_user():
    return UserCreate(
        name="Test User",
        email="test@example.com",
        password="securepassword",  
    )

def test_register_user_success(user_service, mock_repo, mock_refresh_token_service, mock_user):
    mock_repo.get_by_email.return_value = None

    user = user_service.register_user(mock_user)

    assert user.name == mock_user.name
    assert user.email == mock_user.email
    assert user.hashed_password != mock_user.password  # Ensure password is hashed


def test_register_user_failure(user_service, mock_repo, mock_refresh_token_service, mock_user):
    mock_repo.get_by_email.return_value = None
    mock_repo.create.side_effect = Exception("Database error")

    with pytest.raises(HTTPException) as exc_info:
        user_service.register_user(mock_user)

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Failed to register user."

from unittest.mock import MagicMock, patch


def test_login_user_success(user_service, mock_repo, mock_refresh_token_service):
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.hashed_password = hash_password("securepassword")

    mock_repo.get_by_email.return_value = mock_user
    mock_refresh_token_service.create_refresh_token.return_value = "refresh-token"

    payload = UserLogin(
        email="test@example.com",
        password="securepassword"
    )

    access_token, refresh_token = user_service.login_user(payload)
    assert access_token is not None
    assert refresh_token == "refresh-token"

def test_login_user_invalid_email(user_service, mock_repo):
    mock_repo.get_by_email.return_value = None

    payload = UserLogin(
        email="nonexistent@example.com",
        password="securepassword"
    )

    with pytest.raises(HTTPException) as exc_info:
        user_service.login_user(payload)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid email or password."