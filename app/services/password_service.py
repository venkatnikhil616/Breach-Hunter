from typing import Dict, Any

from app.core.entropy_engine import calculate_entropy
from app.core.pattern_detector import analyze_patterns
from app.core.scoring_engine import calculate_score
from app.services.breach_service import check_breach


# Orchestrates full password analysis
async def analyze_password(password: str) -> Dict[str, Any]:
    # Entropy calculation
    entropy = calculate_entropy(password)

    # Pattern detection (warnings/penalties)
    pattern_result = analyze_patterns(password)

    # Scoring
    score_result = calculate_score(password, entropy, pattern_result)

    # Feedback construction
    suggestions = []

    if len(password) < 8:
        suggestions.append("Use at least 8 characters")
    if len(password) < 12:
        suggestions.append("Consider using 12+ characters")

    import re
    if not re.search(r"[A-Z]", password):
        suggestions.append("Add uppercase letters")
    if not re.search(r"[a-z]", password):
        suggestions.append("Add lowercase letters")
    if not re.search(r"\d", password):
        suggestions.append("Include numbers")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-\\/\[\]=+`~;']", password):
        suggestions.append("Add special characters")

    # Breach check (async)
    breach_result = await check_breach(password)

    return {
        "strength": {
            "score": score_result["score"],
            "entropy": entropy,
            "strength": score_result["strength"],
        },
        "feedback": {
            "suggestions": suggestions,
            "warnings": pattern_result.get("warnings", []),
        },
        "breached": breach_result,
    }
