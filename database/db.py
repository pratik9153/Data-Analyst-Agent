
"""SQLite connection and initialization."""

import sqlite3
from pathlib import Path


DEFAULT_DB_PATH = Path("data") / "data_analyst.db"


def get_connection(db_path: str | Path = DEFAULT_DB_PATH):
    """Create and return a SQLite database connection."""
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(path, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_database(
    db_path: str | Path = DEFAULT_DB_PATH,
) -> None:
    """Create the database tables if they do not exist."""
    with get_connection(db_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dataset_name TEXT NOT NULL,
                user_question TEXT NOT NULL,
                verification_status TEXT NOT NULL,
                report_path TEXT,
                final_answer TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_analysis_history_created_at
            ON analysis_history(created_at)
            """
        )
