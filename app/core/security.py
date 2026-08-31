from datetime import datetime, timedelta, timezone
import jwt
from app.core.config import settings
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher

# PasswordHash handles hashing, salting, and verification automatically
password_hash = PasswordHash((Argon2Hasher(), BcryptHasher()))


def hash_password(password: str) -> str:
    """Generate a secure cryptographic hash from a plain text password."""
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if the provided plain text matches the stored hash."""
    return password_hash.verify(plain_password, hashed_password)

COMMON_PASSWORDS = {
    "password",
    "password123",
    "12345678",
    "qwerty123",
}


def validate_password(password: str) -> str:
    if password.lower() in COMMON_PASSWORDS:
        raise ValueError("Password is too common.")

    return password

def create_access_token(user_id: int) -> str:
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(
            minutes=settings.access_token_expire_minutes
        ),
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )