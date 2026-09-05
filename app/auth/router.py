from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.repository import RefreshTokenRepository
from app.auth.service import RefreshTokenService
from app.db.database import get_db
from app.user.schema import RefreshTokenRequest, TokenResponse


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


def get_refresh_token_service(
    db: Session = Depends(get_db),
) -> RefreshTokenService:
    repo = RefreshTokenRepository(db)
    return RefreshTokenService(repo , db)


@router.post("/refresh", response_model=TokenResponse)
def refresh_access_token(
    payload: RefreshTokenRequest,
    service: RefreshTokenService = Depends(get_refresh_token_service),
) -> TokenResponse:

    access_token, refresh_token = service.refresh_access_token(
        payload.refresh_token
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )