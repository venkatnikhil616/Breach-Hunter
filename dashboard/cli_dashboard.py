import json
import time
from typing import Dict, Any

import httpx


API_URL = "http://127.0.0.1:8000/api/analyze"


def _print_header():
    print("=" * 50)
    print(" Password Security CLI Dashboard ")
    print("=" * 50)


def _print_result(result: Dict[str, Any]):
    strength = result.get("strength", {})
    feedback = result.get("feedback", {})
    breached = result.get("breached", {})

    print("\n--- Analysis Result ---")
    print(f"Score     : {strength.get('score')}")
    print(f"Entropy   : {strength.get('entropy')}")
    print(f"Strength  : {strength.get('strength')}")

    print("\nSuggestions:")
    for s in feedback.get("suggestions", []):
        print(f" - {s}")

    print("\nWarnings:")
    for w in feedback.get("warnings", []):
        print(f" - {w}")

    print("\nBreach Status:")
    if breached:
        print(f" - Breached     : {breached.get('breached')}")
        print(f" - Count        : {breached.get('breach_count')}")
    else:
        print(" - Not checked")

    print("-" * 50)


def analyze_password(password: str):
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(API_URL, json={"password": password})
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        print(f"[ERROR] API request failed: {e}")
        return None


def main():
    _print_header()

    while True:
        password = input("\nEnter password (or 'exit'): ").strip()

        if password.lower() in {"exit", "quit"}:
            print("Exiting...")
            break

        if not password:
            print("Password cannot be empty")
            continue

        print("\nAnalyzing...")
        time.sleep(0.5)

        result = analyze_password(password)
        if result:
            _print_result(result)
        else:
            print("Failed to analyze password.")


if __name__ == "__main__":
    main()
