import pytest

from app.services.breach_service import check_breach


@pytest.mark.asyncio
async def test_empty_password():
    result = await check_breach("")
    assert result["breached"] is False
    assert result["breach_count"] is None


@pytest.mark.asyncio
async def test_known_breached_password():
    # "password" is known to be breached many times
    result = await check_breach("password")
    assert result["breached"] is True
    assert result["breach_count"] is not None
    assert result["breach_count"] > 0


@pytest.mark.asyncio
async def test_unlikely_password():
    # Highly unique password (very low chance of being breached)
    result = await check_breach("XyZ!9#pQ2@LmN7$k")
    assert "breached" in result
    assert "breach_count" in result


@pytest.mark.asyncio
async def test_response_structure():
    result = await check_breach("test123")          
    assert isinstance(result, dict)
    assert "breached" in result
    assert "breach_count" in result
