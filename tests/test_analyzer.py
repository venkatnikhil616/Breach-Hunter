import pytest

from app.core.password_analyzer import analyze_password


def test_empty_password():
    result = analyze_password("")
    assert "strength" in result
    assert result["strength"]["score"] >= 0


def test_weak_password():
    result = analyze_password("12345")
    assert result["strength"]["strength"] in ["Weak", "Moderate"]
    assert result["strength"]["score"] < 50


def test_strong_password():
    result = analyze_password("Str0ng!Passw0rd#2026")
    assert result["strength"]["strength"] == "Strong"
    assert result["strength"]["score"] >= 70


def test_entropy_presence():
    result = analyze_password("Example123!")
    assert "entropy" in result["strength"]
    assert result["strength"]["entropy"] > 0


def test_feedback_structure():
    result = analyze_password("password")
    assert "feedback" in result
    assert "suggestions" in result["feedback"]
    assert "warnings" in result["feedback"]


def test_common_password_warning():
    result = analyze_password("password")
    warnings = result["feedback"]["warnings"]
    assert any("Common" in w for w in warnings)


def test_repeated_characters_warning():
    result = analyze_password("aaaBBB111")
    warnings = result["feedback"]["warnings"]
    assert any("Repeated" in w for w in warnings)


def test_special_characters_increase_score():
    weak = analyze_password("Password123")
    strong = analyze_password("Password123!")
    assert strong["strength"]["score"] >= weak["strength"]["score"]
  
