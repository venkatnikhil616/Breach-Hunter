import math
import re
from typing import Dict

# Character set sizes
CHARSETS = {
    "lower": 26,
    "upper": 26,
    "digits": 10,
    "symbols": 32,
}

# Detect which character sets are used
def detect_charsets(password: str) -> Dict[str, bool]:
    return {
        "lower": bool(re.search(r"[a-z]", password)),
        "upper": bool(re.search(r"[A-Z]", password)),
        "digits": bool(re.search(r"\d", password)),
        "symbols": bool(re.search(r"[!@#$%^&*(),.?\":{}|<>_\-\\/\[\]=+`~;']", password)),
    }

# Calculates total charset size
def calculate_charset_size(password: str) -> int:
    used = detect_charsets(password)
    size = sum(CHARSETS[key] for key, present in used.items() if present)
    return size if size > 0 else 1

# Shannon entropy approximation: log2(N^L) = L * log2(N)
def calculate_entropy(password: str) -> float:
    length = len(password)
    charset_size = calculate_charset_size(password)
    entropy = length * math.log2(charset_size)
    return round(entropy, 2)

# Normalize entropy into a 0–100 score
def entropy_score(entropy: float) -> int:
    # Typical strong passwords ~80+ bits
    score = min(int((entropy / 80) * 100), 100)
    return max(score, 0)

# Human-readable entropy strength classification
def entropy_strength(entropy: float) -> str:
    if entropy < 40:
        return "Very Weak"
    elif entropy < 60:
        return "Weak"
    elif entropy < 80:
        return "Moderate"
    elif entropy < 100:
        return "Strong"
    return "Very Strong"
