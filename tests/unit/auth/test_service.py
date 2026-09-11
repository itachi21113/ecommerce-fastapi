import pytest
from unittest.mock import MagicMock
from datetime import datetime, timezone
from fastapi import HTTPException

from app.auth.service import RefreshTokenService


@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def service(mock_repo, mock_db):
    return RefreshTokenService(
        repo=mock_repo,
        db=mock_db,
    )


@pytest.fixture
def mock_user():
    user = MagicMock()
    user.id = 1
    return user


def test_create_refresh_token(service, mock_repo, mock_user):
    raw_token = service.create_refresh_token(mock_user)

    assert isinstance(raw_token, str)
    assert raw_token

    mock_repo.create.assert_called_once()


def test_validate_refresh_token_rejects_invalid_token(service, mock_repo):
    mock_repo.get_by_token_hash.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        service.validate_refresh_token("invalid-token")

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid refresh token."


def test_validate_refresh_token_rejects_revoked_token(service, mock_repo):
    mock_refresh_token = MagicMock()
    mock_refresh_token.revoked_at = "2024-01-01T00:00:00Z"
    mock_refresh_token.user_id = 1

    mock_repo.get_by_token_hash.return_value = mock_refresh_token

    with pytest.raises(HTTPException) as exc_info:
        service.validate_refresh_token("valid-but-revoked-token")

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Refresh token has been revoked."

def test_validate_refresh_token_rejects_expired_token(service, mock_repo):
    mock_refresh_token = MagicMock()
    mock_refresh_token.revoked_at = None
    mock_refresh_token.expires_at = datetime.now(timezone.utc).replace(year=2020)  # Past date

    mock_repo.get_by_token_hash.return_value = mock_refresh_token

    with pytest.raises(HTTPException) as exc_info:
        service.validate_refresh_token("valid-but-expired-token")

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Refresh token has expired."