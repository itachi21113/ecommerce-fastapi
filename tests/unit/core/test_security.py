# tests/unit/core/test_security.py

import pytest

from app.core.security import (
    hash_password,
    validate_password,
    verify_password,
    create_access_token,
    decode_access_token,
)

def test_validate_password_accepts_valid_password():
    validate_password("my-strong-password")

def test_validate_password_rejects_common_password():
    with pytest.raises(ValueError):
        validate_password("password")

def test_hash_password_does_not_return_plaintext():
    password = "my-strong-password"

    hashed_password = hash_password(password)

    assert hashed_password != password

def test_hashed_password_can_be_verified():
    password = "my-strong-password"

    hashed_password = hash_password(password)

    assert verify_password(password, hashed_password) is True

def test_verify_password_returns_false_for_wrong_password():
    password = "my-strong-password"
    wrong_password = "wrong-password"

    hashed_password = hash_password(password)

    assert verify_password(wrong_password, hashed_password) is False


def test_verify_password_returns_false_for_invalid_hash():
    password = "my-strong-password"

    invalid_hash = "$argon2id$v=19$m=65536,t=3,p=4$invalidsalt$invalidhash"

    assert verify_password(password, invalid_hash) is False

def test_validate_password_accepts_password_at_minimum_length():
    min_length_password = "a" * 8  # Assuming minimum length is 8
    validate_password(min_length_password)

@pytest.mark.parametrize(
    "password",
    [
        "password",
        "password123",
        "12345678",
        "qwerty123",
    ],
)
def test_validate_password_rejects_common_passwords(password):
    with pytest.raises(ValueError):
        validate_password(password)

def test_hash_password_produces_different_hashes_for_same_password():
    password = "my-strong-password"

    hash1 = hash_password(password)
    hash2 = hash_password(password)

    assert hash1 != hash2

def test_create_access_token_produces_decodable_token():
    
    user_id = 123
    token = create_access_token(user_id)
    decoded_token = decode_access_token(token)
    assert decoded_token["sub"] == str(user_id)

def test_decode_access_token_returns_none_for_invalid_token():
    invalid_token = "invalid.token.string"
    decoded_token = decode_access_token(invalid_token)
    assert decoded_token is None

def test_create_access_token_contains_issued_at_and_expiration():
    user_id = 123
    token = create_access_token(user_id)
    decoded_token = decode_access_token(token)
    assert "iat" in decoded_token
    assert "exp" in decoded_token