import hashlib
import hmac
import os
import base64
from typing import Tuple


# Generate random salt
def generate_salt(length: int = 16) -> str:
    return base64.urlsafe_b64encode(os.urandom(length)).decode("utf-8")


# Hash password using PBKDF2-HMAC (SHA256)
def hash_password(password: str, salt: str, iterations: int = 100_000) -> str:
    dk = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        iterations,
    )
    return base64.urlsafe_b64encode(dk).decode("utf-8")


# Verify password against stored hash
def verify_password(
    password: str,
    salt: str,
    stored_hash: str,
    iterations: int = 100_000,
) -> bool:
    new_hash = hash_password(password, salt, iterations)
    return hmac.compare_digest(new_hash, stored_hash)


# Convenience: create salt + hash together
def create_password_hash(password: str) -> Tuple[str, str]:
    salt = generate_salt()
    hashed = hash_password(password, salt)
    return salt, hashed


# SHA-1 hash (used for HIBP k-anonymity)
def sha1_hash(password: str) -> str:
    return hashlib.sha1(password.encode("utf-8")).hexdigest().upper()


# SHA-256 hash (general purpose)
def sha256_hash(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


# HMAC-SHA256 (for signing)
def hmac_sha256(key: str, message: str) -> str:
    return hmac.new(
        key.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
