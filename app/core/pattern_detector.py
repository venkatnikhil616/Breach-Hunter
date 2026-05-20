import re
from typing import Dict, List


# Common weak patterns
COMMON_PATTERNS = [
    "password",
    "123456",
    "qwerty",
    "admin",
    "letmein",
    "welcome",
]


# Keyboard sequences (basic)
KEYBOARD_SEQUENCES = [
    "qwerty",
    "asdfgh",
    "zxcvbn",
    "12345",
    "67890",
]


# Detect repeated characters (aaa, 1111)
def detect_repeated(password: str) -> bool:
    return bool(re.search(r"(.)\1{2,}", password))


# Detect sequential characters (abc, 123)
def detect_sequences(password: str) -> bool:
    sequences = [
        "abcdefghijklmnopqrstuvwxyz",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "0123456789"
    ]

    for seq in sequences:
        for i in range(len(seq) - 2):
            sub = seq[i:i+3]
            if sub in password:
                return True
    return False


# Detect keyboard patterns
def detect_keyboard_patterns(password: str) -> bool:
    lower_pass = password.lower()
    return any(pattern in lower_pass for pattern in KEYBOARD_SEQUENCES)


# Detect common passwords
def detect_common(password: str) -> bool:
    return password.lower() in COMMON_PATTERNS


# Detect repeated substrings (e.g., abcabc)
def detect_repeated_patterns(password: str) -> bool:
    return bool(re.search(r"(.+)\1+", password))


# Aggregate all pattern detections
def analyze_patterns(password: str) -> Dict[str, List[str]]:
    warnings: List[str] = []

    if detect_common(password):
        warnings.append("Common password detected")

    if detect_repeated(password):
        warnings.append("Repeated characters detected")

    if detect_sequences(password):
        warnings.append("Sequential characters detected")

    if detect_keyboard_patterns(password):
        warnings.append("Keyboard pattern detected")

    if detect_repeated_patterns(password):
        warnings.append("Repeated pattern detected")

    return {
        "warnings": warnings
    }
