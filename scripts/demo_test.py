from app.services.password_service import analyze_password


def run_demo():
    passwords = [
        "12345",
        "password",
        "Password123",
        "Password123!",
        "Str0ng!Passw0rd#2026"
    ]

    for pwd in passwords:
        print("=" * 50)
        print(f"Password: {pwd}")

        result = analyze_password(pwd)

        print("Score     :", result["strength"]["score"])
        print("Entropy   :", result["strength"]["entropy"])
        print("Strength  :", result["strength"]["strength"])

        print("Suggestions:")
        for s in result["feedback"]["suggestions"]:
            print(" -", s)

        print("Warnings:")
        for w in result["feedback"]["warnings"]:
            print(" -", w)

        print("Breached  :", result["breached"])
        print("=" * 50)


if __name__ == "__main__":
    run_demo()
