
"""Deterministic statistical tools."""

import pandas as pd


def describe_column(
    df: pd.DataFrame,
    column: str,
) -> dict:
    # Check whether the requested column exists
    if column not in df.columns:
        raise ValueError(f"Column not found: {column}")

    # Convert the column to numeric values
    values = pd.to_numeric(
        df[column],
        errors="coerce",
    ).dropna()

    if values.empty:
        raise ValueError(
            f"Column '{column}' has no valid numeric values."
        )

    # Calculate descriptive statistics
    return {
        "column": column,
        "count": int(values.count()),
        "mean": round(float(values.mean()), 4),
        "median": round(float(values.median()), 4),
        "standard_deviation": round(float(values.std()), 4),
        "minimum": round(float(values.min()), 4),
        "maximum": round(float(values.max()), 4),
        "total": round(float(values.sum()), 4),
    }


def correlation(
    df: pd.DataFrame,
    first_column: str,
    second_column: str,
) -> dict:
    # Check that both columns exist
    for column in [first_column, second_column]:
        if column not in df.columns:
            raise ValueError(f"Column not found: {column}")

    # Convert both columns to numeric values
    values = df[[first_column, second_column]].apply(
        pd.to_numeric,
        errors="coerce",
    ).dropna()

    if len(values) < 2:
        raise ValueError(
            "At least two complete rows are required."
        )

    # Correlation is undefined when either column is constant
    if (
        values[first_column].nunique() < 2
        or values[second_column].nunique() < 2
    ):
        raise ValueError(
            "Correlation requires variation in both columns."
        )

    # Calculate Pearson correlation
    result = values[first_column].corr(
        values[second_column]
    )

    return {
        "first_column": first_column,
        "second_column": second_column,
        "method": "pearson",
        "correlation": round(float(result), 4),
        "rows_used": len(values),
    }
