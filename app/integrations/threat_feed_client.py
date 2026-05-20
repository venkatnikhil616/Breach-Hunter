import httpx
from typing import List, Dict, Any, Optional


DEFAULT_TIMEOUT = 10.0


# Generic HTTP GET helper
async def _fetch_json(url: str, headers: Optional[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        try:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError:
            return None


# Example: fetch recent breaches (placeholder endpoint)
async def fetch_recent_breaches(api_url: str, api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    headers = {"User-Agent": "password-security-platform"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    data = await _fetch_json(api_url, headers=headers)
    if not data:
        return []

    # Normalize expected structure
    breaches = []
    for item in data.get("breaches", []):
        breaches.append({
            "name": item.get("name"),
            "domain": item.get("domain"),
            "breach_date": item.get("breach_date"),
            "added_date": item.get("added_date"),
            "pwn_count": item.get("pwn_count"),
            "description": item.get("description"),
        })

    return breaches


# Example: fetch threat indicators (generic feed)
async def fetch_threat_indicators(feed_url: str) -> List[Dict[str, Any]]:
    data = await _fetch_json(feed_url)
    if not data:
        return []

    indicators = []
    for item in data.get("indicators", []):
        indicators.append({
            "type": item.get("type"),
            "value": item.get("value"),
            "confidence": item.get("confidence"),
            "source": item.get("source"),
        })

    return indicators


# Health check for external threat feed
async def check_feed_health(feed_url: str) -> bool:
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        try:
            resp = await client.get(feed_url)
            return resp.status_code == 200
        except httpx.HTTPError:
            return False
