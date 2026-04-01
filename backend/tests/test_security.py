from app.core.security import create_access_token, decode_token, hash_password, verify_password


def test_password_hashing_round_trip() -> None:
    password = "strong-password"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True


def test_access_token_contains_subject() -> None:
    token = create_access_token("42")
    payload = decode_token(token)

    assert payload["sub"] == "42"
