
"""Database persistence operations."""

from pathlib import Path
from typing import Any

from database.db import DEFAULT_DB_PATH, get_connection
from src.utils.exceptions import DatabaseError


def save_analysis(
    dataset_name: str,
    user_question: str,
    verification_status: str,
    report_path: str | None = None,
    final_answer: str | None = None,
    db_path: str | Path = DEFAULT_DB_PATH,
) -> int:
    """Save an analysis run and return its database ID."""
    if not dataset_name.strip():
        raise ValueError("dataset_name cannot be empty.")

    if not user_question.strip():
        raise ValueError("user_question cannot be empty.")

    if not verification_status.strip():
        raise ValueError("verification_status cannot be empty.")

    try:
        with get_connection(db_path) as connection:
            cursor = connection.execute(
                """
                INSERT INTO analysis_history (
                    dataset_name,
                    user_question,
                    verification_status,
                    report_path,
                    final_answer
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    dataset_name,
                    user_question,
                    verification_status,
                    report_path,
                    final_answer,
                ),
            )
            return int(cursor.lastrowid)

    except Exception as error:
        raise DatabaseError(
            f"Could not save analysis: {error}"
        ) from error


def get_analysis_history(
    limit: int = 50,
    db_path: str | Path = DEFAULT_DB_PATH,
) -> list[dict[str, Any]]:
    """Return recent analysis records, newest first."""
    if limit < 1:
        raise ValueError("limit must be at least 1.")

    try:
        with get_connection(db_path) as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM analysis_history
                ORDER BY created_at DESC, id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

            return [dict(row) for row in rows]

    except Exception as error:
        raise DatabaseError(
            f"Could not retrieve analysis history: {error}"
        ) from error


def get_analysis_by_id(
    analysis_id: int,
    db_path: str | Path = DEFAULT_DB_PATH,
) -> dict[str, Any] | None:
    """Retrieve one analysis record by its ID."""
    try:
        with get_connection(db_path) as connection:
            row = connection.execute(
                "SELECT * FROM analysis_history WHERE id = ?",
                (analysis_id,),
            ).fetchone()

            return dict(row) if row is not None else None

    except Exception as error:
        raise DatabaseError(
            f"Could not retrieve analysis: {error}"
        ) from error
