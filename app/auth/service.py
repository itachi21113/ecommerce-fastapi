from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.security import (
    create_refresh_token,
    hash_refresh_token,
)
from app.user.model import RefreshToken, User
from app.auth.repository import RefreshTokenRepository
from datetime import datetime, timezone
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_refresh_token,
)
from app.user.model import RefreshToken
from fastapi import HTTPException, status

class RefreshTokenService:

    def __init__(self, repo: RefreshTokenRepository , db: Session) -> None:
        self.repo = repo
        self.db = db

    def create_refresh_token(self, user: User) -> str:
        raw_token = create_refresh_token()

        token_hash = hash_refresh_token(raw_token)

        refresh_token = RefreshToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=datetime.now(timezone.utc) + timedelta(days=7),
        )

        self.repo.create(refresh_token)

        return raw_token

    def validate_refresh_token(self, raw_token: str) -> RefreshToken:
        token_hash = hash_refresh_token(raw_token)

        refresh_token = self.repo.get_by_token_hash(token_hash)

        if refresh_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token.",
            )

        if refresh_token.revoked_at is not None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has been revoked.",
            )

        if refresh_token.expires_at <= datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has expired.",
            )

        return refresh_token

    def refresh_access_token(
        self,
        raw_token: str,
    ) -> tuple[str, str]:

        refresh_token = self.validate_refresh_token(raw_token)

        user = refresh_token.user

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found.",
            )

        try:
            self.repo.revoke(refresh_token)
            new_refresh_token = self.create_refresh_token(user)
            new_access_token = create_access_token(user.id)
            self.db.commit()
            return new_access_token, new_refresh_token
        
        except Exception :
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to refresh access token.",
            )