import pytest

from app.core.scoring_engine import calculate_score, score_to_strength


def test_low_entropy_score():
    password = "12345"
    entropy = 10.0
    pattern_result = {"warnings": []}

    result = calculate_score(password, entropy, pattern_result)

    assert result["score"] < 40
    assert result["strength"] == "Weak"


def test_high_entropy_score():
    password = "Str0ng!Passw0rd#2026"                 entropy = 90.0
    pattern_result = {"warnings": []}

    result = calculate_score(password, entropy, pattern_result)

    assert result["score"] >= 70
    assert result["strength"] == "Strong"


def test_pattern_penalty():
    password = "password"
    entropy = 40.0
    pattern_result = {"warnings": ["Common password detected"]}

    result = calculate_score(password, entropy, pattern_result)

    assert result["score"] < 50


def test_score_bounds():
    password = "VeryVeryStrongPassword123!@#"
    entropy = 200.0
    pattern_result = {"warnings": []}             
    result = calculate_score(password, entropy, pattern_result)
                                                      assert 0 <= result["score"] <= 100


def test_strength_mapping():
    assert score_to_strength(10) == "Weak"            assert score_to_strength(50) == "Moderate"
    assert score_to_strength(90) == "Strong"
