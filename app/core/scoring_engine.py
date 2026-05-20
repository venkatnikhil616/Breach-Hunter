from typing import Dict


# Clamp value between bounds
def _clamp(value: int, min_value: int = 0, max_value: int = 100) -> int:
    return max(min_value, min(max_value, value))


# Convert entropy (bits) to score contribution (0–50)
def _entropy_component(entropy: float) -> int:
    # 80 bits ≈ strong → maps to full 50 points
    return _clamp(int((entropy / 80.0) * 50), 0, 50)


# Length-based score (0–20)
def _length_component(length: int) -> int:
    score = 0
    if length >= 8:
        score += 10
    if length >= 12:
        score += 5
    if length >= 16:
        score += 5
    return score


# Character variety score (0–30)
def _variety_component(password: str) -> int:
    import re

    score = 0
    if re.search(r"[a-z]", password):
        score += 7
    if re.search(r"[A-Z]", password):
        score += 7
    if re.search(r"\d", password):
        score += 7
    if re.search(r"[!@#$%^&*(),.?\":{}|<>_\-\\/\[\]=+`~;']", password):
        score += 9
    return score


# Penalties based on detected patterns
def _pattern_penalty(pattern_result: Dict) -> int:
    warnings = pattern_result.get("warnings", [])

    penalty = 0
    for w in warnings:
        if "Common password" in w:
            penalty += 40
        elif "Repeated characters" in w:
            penalty += 10
        elif "Sequential characters" in w:
            penalty += 10
        elif "Keyboard pattern" in w:
            penalty += 10
        elif "Repeated pattern" in w:
            penalty += 10

    return penalty


# Convert numeric score to label
def score_to_strength(score: int) -> str:
    if score < 40:
        return "Weak"
    elif score < 70:
        return "Moderate"
    else:
        return "Strong"


# Main scoring function
def calculate_score(password: str, entropy: float, pattern_result: Dict) -> Dict:
    length_score = _length_component(len(password))
    variety_score = _variety_component(password)
    entropy_score = _entropy_component(entropy)

    base_score = length_score + variety_score + entropy_score

    penalty = _pattern_penalty(pattern_result)

    final_score = _clamp(base_score - penalty)

    return {
        "score": final_score,
        "strength": score_to_strength(final_score)
    }
