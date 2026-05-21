"""
Main entry point for Password Security Platform   """

import re
import uvicorn
from time import sleep

from rich.console import Console
from rich.panel import Panel
from rich.progress import track

from app.api.app import create_app
from app.config.config import get_settings
from app.utils.logger import setup_logging

console = Console()

def check_password_strength(password):
    score = 0
    remarks = []

    # Length check
    if len(password) >= 12:
        score += 25
    elif len(password) >= 8:
        score += 15
    else:
        remarks.append("Password is too short")

    # Uppercase letters
    if re.search(r"[A-Z]", password):
        score += 15
    else:
        remarks.append("Add uppercase letters")

    # Lowercase letters
    if re.search(r"[a-z]", password):
        score += 15
    else:
        remarks.append("Add lowercase letters")

    # Numbers
    if re.search(r"\d", password):
        score += 20
    else:
        remarks.append("Add numbers")

    # Special characters
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 25
    else:
        remarks.append("Add special characters")

    # Final strength rating
    if score >= 80:
        strength = "Very Strong"
    elif score >= 60:
        strength = "Strong"
    elif score >= 40:
        strength = "Medium"
    else:
        strength = "Weak"

    return score, strength, remarks

def password_cli():
    while True:
        console.print("\n[bold cyan]=== Breach Hunter Password Analyzer ===[/bold cyan]\n")

        password = console.input(
            "[bold yellow]Enter password to analyze (type 'exit' to quit):[/bold yellow] "
        )

        if password.lower() == "exit":
            console.print("\n[bold red]Exiting Password Analyzer...[/bold red]")
            break

        score, strength, remarks = check_password_strength(password)

        console.print("\n[bold green]=== Analysis Result ===[/bold green]")
        console.print(f"[bold]Strength :[/bold] {strength}")
        console.print(f"[bold]Score    :[/bold] {score}/100")

        if remarks:
            console.print("\n[bold red]Recommendations:[/bold red]")
            for r in remarks:
                console.print(f"- {r}")

        console.print("\n[bold cyan]Ready for next password...[/bold cyan]")

def run_api():
    # Load settings
    settings = get_settings()

    # Setup logging
    setup_logging(settings.LOG_LEVEL)

    # Create FastAPI app
    app = create_app()

    # Run server
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )

def main():
    console.clear()

    # Animated loading
    for _ in track(range(30), description="Initializing Breach Hunter..."):
        sleep(0.03)

    console.clear()

    # Banner
    banner = """
██████╗ ██████╗ ███████╗ █████╗  ██████╗██╗  ██╗
██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔════╝██║  ██║
██████╔╝██████╔╝█████╗  ███████║██║     ███████║
██╔══██╗██╔══██╗██╔══╝  ██╔══██║██║     ██╔══██║
██████╔╝██║  ██║███████╗██║  ██║╚██████╗██║  ██║
╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
"""

    console.print(f"[bold cyan]{banner}[/bold cyan]")

    console.print(
        Panel.fit(
            "[1] Password Strength Checker\n[2] Run API Server",
            title="Breach Hunter Menu",
            border_style="green"
        )
    )

    choice = console.input("\n[bold yellow]Select option:[/bold yellow] ")

    if choice == "1":
        password_cli()

    elif choice == "2":
        console.print("\n[bold green]Starting API Server...[/bold green]\n")
        sleep(1)
        run_api()

    else:
        console.print("[bold red]Invalid option[/bold red]")

if __name__ == "__main__":
    main()
