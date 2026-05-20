import hashlib
from typing import Optional

import httpx


HIBP_RANGE_URL = "https://api.pwnedpasswords.com/range/{}"


# Generate SHA-1 hash (uppercase hex)
def sha1_hash(password: str) -> str:
    return hashlib.sha1(password.encode("utf-8")).hexdigest().upper()


# Fetch hash suffix list from HIBP
async def fetch_range(prefix: str) -> str:
    async with httpx.AsyncClient(timeout=10.0) as client:
        headers = {
            "User-Agent": "password-security-platform",
            "Add-Padding": "true",
        }
        response = await client.get(HIBP_RANGE_URL.format(prefix), headers=headers)
        response.raise_for_status()
        return response.text


# Check if hash suffix exists in response
def parse_pwned_count(suffix: str, response_text: str) -> int:
    for line in response_text.splitlines():
        try:
            hash_suffix, count = line.split(":")
            if hash_suffix.strip().upper() == suffix:
                return int(count.strip())
        except ValueError:
            continue
    return 0


# Public helper
async def check_password_pwned(password: str) -> Optional[int]:
    if not password:
        return None

    full_hash = sha1_hash(password)
    prefix, suffix = full_hash[:5], full_hash[5:]

    try:
        response_text = await fetch_range(prefix)
        count = parse_pwned_count(suffix, response_text)
        return count if count > 0 else 0
    except httpx.HTTPError:
        return None
