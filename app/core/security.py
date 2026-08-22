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