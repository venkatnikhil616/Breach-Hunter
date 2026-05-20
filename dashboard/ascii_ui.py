import shutil
from typing import List


# Get terminal width
def _get_width() -> int:
    return shutil.get_terminal_size((80, 20)).columns


# Center text
def center_text(text: str) -> str:
    width = _get_width()
    return text.center(width)


# Divider line
def divider(char: str = "=") -> str:
    return char * _get_width()


# Boxed text
def box(text: str) -> str:
    lines = text.split("\n")
    width = max(len(line) for line in lines) + 4

    top = "+" + "-" * (width - 2) + "+"
    bottom = top

    content = []
    for line in lines:
        content.append(f"| {line.ljust(width - 4)} |")

    return "\n".join([top] + content + [bottom])


# Progress bar
def progress_bar(value: int, max_value: int = 100, length: int = 30) -> str:
    percent = min(max(value / max_value, 0), 1)
    filled = int(length * percent)
    bar = "#" * filled + "-" * (length - filled)
    return f"[{bar}] {int(percent * 100)}%"


# Colored text (ANSI)
def color_text(text: str, color: str) -> str:
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m",
    }
    return f"{colors.get(color, colors['white'])}{text}{colors['reset']}"


# Status color helper
def strength_color(strength: str) -> str:
    mapping = {
        "Weak": "red",
        "Moderate": "yellow",
        "Strong": "green",
    }
    return mapping.get(strength, "white")


# Render list nicely
def render_list(items: List[str], prefix: str = "- ") -> str:
    if not items:
        return "  (none)"
    return "\n".join(f"{prefix}{item}" for item in items)
