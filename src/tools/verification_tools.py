
"""Independent result verification."""

import math
import pandas as pd


def verify_metric(
    df: pd.DataFrame,
    column: str,
    operation: str,
    reported_value: int | float,
    tolerance: float = 0.0001,
) -> dict:
    # Check that the column exists
    if column not in df.columns:
        return {
            "passed": False,
            "reason": f"Column not found: {column}",
        }

    # Check that the reported value is a valid number
    if (
        isinstance(reported_value, bool)
        or not isinstance(reported_value, (int, float))
        or not math.isfinite(reported_value)
    ):
        return {
            "passed": False,
            "reason": "Reported value must be a finite number.",
        }

    # Count operations can work with non-numeric columns
    operation = operation.lower().strip()

    if operation == "count":
        expected_value = int(df[column].count())

    elif operation == "nunique":
        expected_value = int(df[column].nunique())

    else:
        # Convert numeric data and ignore invalid or missing values
        values = pd.to_numeric(
            df[column],
            errors="coerce",
        ).dropna()

        if values.empty:
            return {
                "passed": False,
                "reason": "No valid numeric values to verify.",
            }

        # Recalculate the expected result
        if operation == "sum":
            expected_value = float(values.sum())
        elif operation == "mean":
            expected_value = float(values.mean())
        elif operation == "median":
            expected_value = float(values.median())
        elif operation == "min":
            expected_value = float(values.min())
        elif operation == "max":
            expected_value = float(values.max())
        else:
            return {
                "passed": False,
                "reason": f"Unsupported operation: {operation}",
            }

    # Compare the reported result with the recalculated value
    passed = math.isclose(
        float(reported_value),
        float(expected_value),
        rel_tol=tolerance,
        abs_tol=tolerance,
    )

    return {
        "passed": passed,
        "column": column,
        "operation": operation,
        "reported_value": reported_value,
        "expected_value": expected_value,
        "reason": (
            "Result matches recalculation."
            if passed
            else "Reported value does not match recalculation."
        ),
    }
