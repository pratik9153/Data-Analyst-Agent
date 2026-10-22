
"""Shared utility functions."""

from pathlib import Path
from typing import Any


def ensure_directory(directory: str | Path) -> Path:
    """Create a directory if it does not exist."""
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path


def format_number(value: Any, decimals: int = 2) -> str:
    """Format numeric values for display."""
    if value is None:
        return "N/A"

    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)

    if number != number:  # NaN check
        return "N/A"

    return f"{number:,.{decimals}f}"


def validate_file_exists(file_path: str | Path) -> Path:
    """Return a file path if it exists and points to a file."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if not path.is_file():
        raise ValueError(f"Expected a file, received: {path}")

    return path
