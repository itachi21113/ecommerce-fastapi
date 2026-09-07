from sqlalchemy import select, update
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.user.model import RefreshToken


class RefreshTokenRepository:

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, refresh_token: RefreshToken) -> RefreshToken:
        self.db.add(refresh_token)
        self.db.flush()
        return refresh_token

    def get_by_token_hash(
        self,
        token_hash: str,
    ) -> RefreshToken | None:
        stmt = select(RefreshToken).where(
            RefreshToken.token_hash == token_hash
        )

        return self.db.execute(stmt).scalar_one_or_none()

    def revoke(self, refresh_token: RefreshToken) -> RefreshToken:
        refresh_token.revoked_at = datetime.now(timezone.utc)

        self.db.flush()
        return refresh_token

    def revoke_all_tokens_for_user(self, user_id: int) -> None:
        stmt = (
            update(RefreshToken)
            .where(
                RefreshToken.user_id == user_id,
                RefreshToken.revoked_at.is_(None)
                )
            .values(
                revoked_at=datetime.now(timezone.utc)
                )  
        )
        self.db.execute(stmt)
        self.db.flush()