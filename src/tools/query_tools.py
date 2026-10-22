
"""Approved dataset query operations."""

import pandas as pd


def calculate_metric(
    df: pd.DataFrame,
    column: str,
    operation: str,
) -> dict:
    # Make sure the requested column exists
    if column not in df.columns:
        raise ValueError(f"Column not found: {column}")

    # Select the requested operation
    operation = operation.lower().strip()

    # Count all rows with a non-missing value
    if operation == "count":
        value = int(df[column].count())

    # Count distinct non-missing values
    elif operation == "nunique":
        value = int(df[column].nunique())

    else:
        # These operations require numeric data
        numeric_values = pd.to_numeric(
            df[column],
            errors="coerce",
        ).dropna()

        if numeric_values.empty:
            raise ValueError(
                f"Column '{column}' has no valid numeric values."
            )

        if operation == "sum":
            value = float(numeric_values.sum())

        elif operation == "mean":
            value = float(numeric_values.mean())

        elif operation == "median":
            value = float(numeric_values.median())

        elif operation == "min":
            value = float(numeric_values.min())

        elif operation == "max":
            value = float(numeric_values.max())

        else:
            raise ValueError(
                f"Unsupported operation: {operation}"
            )

    # Return the calculation and its source information
    return {
        "column": column,
        "operation": operation,
        "value": round(value, 4) if isinstance(value, float) else value,
        "valid_count": int(df[column].count()),
    }


def group_metric(
    df: pd.DataFrame,
    group_by: str,
    column: str,
    operation: str = "sum",
) -> dict:
    # Check that both columns exist
    if group_by not in df.columns:
        raise ValueError(f"Grouping column not found: {group_by}")

    if column not in df.columns:
        raise ValueError(f"Column not found: {column}")

    operation = operation.lower().strip()

    if operation not in {"sum", "mean", "count", "min", "max"}:
        raise ValueError(
            f"Unsupported grouping operation: {operation}"
        )

    # Convert the value column when a numeric operation is needed
    working_df = df[[group_by, column]].copy()

    if operation != "count":
        working_df[column] = pd.to_numeric(
            working_df[column],
            errors="coerce",
        )

    # Exclude missing group labels so they are not mistaken for real groups
    working_df = working_df.dropna(subset=[group_by])

    grouped = working_df.groupby(group_by)[column]

    if operation == "sum":
        result = grouped.sum(min_count=1)
    elif operation == "mean":
        result = grouped.mean()
    elif operation == "count":
        result = grouped.count()
    elif operation == "min":
        result = grouped.min()
    else:
        result = grouped.max()

    # Return results as ordinary Python values
    return {
        "group_by": group_by,
        "column": column,
        "operation": operation,
        "results": {
            str(key): round(float(value), 4)
            if pd.notna(value) and isinstance(value, (int, float))
            else value
            for key, value in result.items()
            if pd.notna(value)
        },
    }
