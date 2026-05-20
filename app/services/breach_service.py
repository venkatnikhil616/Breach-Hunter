import hashlib
from typing import Dict, Optional

import httpx


HIBP_RANGE_URL = "https://api.pwnedpasswords.com/range/{}"


# SHA-1 hash of password (uppercase hex)
def _sha1_hash(password: str) -> str:
    return hashlib.sha1(password.encode("utf-8")).hexdigest().upper()


# Query HIBP k-Anonymity API
async def _query_hibp(prefix: str) -> str:
    async with httpx.AsyncClient(timeout=10.0) as client:
        headers = {
            "User-Agent": "password-security-platform",
            "Add-Padding": "true",  # optional privacy padding
        }
        resp = await client.get(HIBP_RANGE_URL.format(prefix), headers=headers)
        resp.raise_for_status()
        return resp.text


# Parse HIBP response and find match count
def _parse_response(suffix: str, body: str) -> int:
    # Each line: HASH_SUFFIX:COUNT
    for line in body.splitlines():
        try:
            hash_suffix, count = line.split(":")
            if hash_suffix.strip().upper() == suffix:
                return int(count.strip())
        except ValueError:
            continue
    return 0


# Public API
async def check_breach(password: str) -> Dict[str, Optional[int]]:
    """
    Returns:
    {
        "breached": bool,
        "breach_count": int | None
    }
    """
    if not password:
        return {"breached": False, "breach_count": None}

    full_hash = _sha1_hash(password)
    prefix, suffix = full_hash[:5], full_hash[5:]

    try:
        body = await _query_hibp(prefix)
        count = _parse_response(suffix, body)
        return {
            "breached": count > 0,
            "breach_count": count if count > 0 else None,
        }
    except httpx.HTTPError:
        # Fail-safe: don't block analysis if API fails
        return {"breached": False, "breach_count": None}
