from datetime import datetime
from typing import Dict, Any


# Generate a structured report from analysis result
def generate_report(password: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "password_length": len(password),
        "strength": analysis.get("strength", {}),
        "feedback": analysis.get("feedback", {}),
        "breached": analysis.get("breached", {}),
        "summary": _build_summary(analysis),
    }


# Create a human-readable summary
def _build_summary(analysis: Dict[str, Any]) -> str:
    strength = analysis.get("strength", {}).get("strength", "Unknown")
    score = analysis.get("strength", {}).get("score", 0)
    breached = analysis.get("breached", {}).get("breached", False)

    if breached:
        return f"Password is {strength} (score: {score}) and has been found in data breaches."

    if strength == "Strong":
        return f"Password is strong (score: {score}) and not found in known breaches."

    return f"Password is {strength} (score: {score}). Improvement is Needed।"
