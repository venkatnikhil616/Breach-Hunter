import math
import re
from typing import Dict, List


# Determine approximate character set size based on used character classes
def _charset_size(password: str) -> int:
    size = 0
    if re.search(r"[a-z]", password):
        size += 26
    if re.search(r"[A-Z]", password):
        size += 26
    if re.search(r"\d", password):
        size += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>_\-\\/\[\]=+`~;']", password):
        size += 32
    return size or 1


# Calculate entropy using log2(charset_size^length)
def _entropy(password: str) -> float:
    charset = _charset_size(password)
    return round(len(password) * math.log2(charset), 2)


# Compute score (0–100) based on rules + entropy contribution
def _score(password: str, entropy: float) -> int:
    score = 0

    # Length scoring
    if len(password) >= 8:
        score += 20
    if len(password) >= 12:
        score += 10

    # Character variety scoring
    if re.search(r"[a-z]", password):
        score += 10
    if re.search(r"[A-Z]", password):
        score += 10
    if re.search(r"\d", password):
        score += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>_\-\\/\[\]=+`~;']", password):
        score += 10

    # Entropy contribution (capped)
    score += min(int(entropy / 2), 30)

    return min(score, 100)


# Convert numeric score to label
def _strength_label(score: int) -> str:
    if score < 40:
        return "Weak"
    elif score < 70:
        return "Moderate"
    return "Strong"


# Generate suggestions and warnings
def _feedback(password: str) -> Dict[str, List[str]]:
    suggestions: List[str] = []
    warnings: List[str] = []

    if len(password) < 8:
        suggestions.append("Use at least 8 characters")

    if not re.search(r"[A-Z]", password):
        suggestions.append("Add uppercase letters")

    if not re.search(r"[a-z]", password):
        suggestions.append("Add lowercase letters")

    if not re.search(r"\d", password):
        suggestions.append("Include numbers")

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-\\/\[\]=+`~;']", password):
        suggestions.append("Add special characters")

    # Common weak passwords
    if password.lower() in {"password", "123456", "qwerty", "admin"}:
        warnings.append("Common password detected")

    # Repeated characters (e.g., aaa, 111)
    if re.search(r"(.)\1{2,}", password):
        warnings.append("Repeated characters detected")

    return {"suggestions": suggestions, "warnings": warnings}


# Main function used by API
def analyze_password(password: str):
    ent = _entropy(password)
    score = _score(password, ent)
    strength = _strength_label(score)
    feedback = _feedback(password)

    return {
        "strength": {
            "score": score,
            "entropy": ent,
            "strength": strength,
        },
        "feedback": feedback,
        "breached": None,  # placeholder for future breach integration
  }
