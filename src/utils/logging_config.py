
"""Application logging configuration."""

import logging
from pathlib import Path


def setup_logging(
    log_dir: str = "logs",
    log_level: int = logging.INFO,
) -> None:
    """Configure console and file logging."""
    directory = Path(log_dir)
    directory.mkdir(parents=True, exist_ok=True)

    log_file = directory / "app.log"

    logging.basicConfig(
        level=log_level,
        format=(
            "%(asctime)s | %(levelname)s | "
            "%(name)s | %(message)s"
        ),
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file, encoding="utf-8"),
        ],
        force=True,
    )
