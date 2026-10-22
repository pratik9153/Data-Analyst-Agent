
"""Auditable data-cleaning operations."""

import pandas as pd


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    # Work on a copy so the original data stays unchanged
    cleaned_df = df.copy()

    # Make column names lowercase and replace spaces with underscores
    cleaned_df.columns = [
        str(column).strip().lower().replace(" ", "_")
        for column in cleaned_df.columns
    ]

    # Reject duplicate column names created by cleaning
    if cleaned_df.columns.duplicated().any():
        raise ValueError(
            "Cleaning created duplicate column names."
        )

    return cleaned_df


def remove_duplicate_rows(
    df: pd.DataFrame,
    keep: str = "first",
) -> tuple[pd.DataFrame, dict]:
    # Validate the duplicate-handling option
    if keep not in {"first", "last", False}:
        raise ValueError(
            "keep must be 'first', 'last', or False."
        )

    # Create a cleaned copy
    cleaned_df = df.drop_duplicates(keep=keep).copy()

    # Record what changed
    details = {
        "original_rows": len(df),
        "cleaned_rows": len(cleaned_df),
        "removed_rows": len(df) - len(cleaned_df),
    }

    return cleaned_df, details


def fill_missing_values(
    df: pd.DataFrame,
    columns: list[str],
    strategy: str = "median",
) -> tuple[pd.DataFrame, dict]:
    # Validate the selected strategy
    if strategy not in {"mean", "median", "mode", "constant"}:
        raise ValueError(
            "strategy must be mean, median, mode, or constant."
        )

    # Check that the requested columns exist
    missing_columns = [
        column for column in columns if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Columns not found: {missing_columns}"
        )

    # Make a copy before changing values
    cleaned_df = df.copy()
    changes = {}

    for column in columns:
        missing_count = int(cleaned_df[column].isna().sum())

        # Skip columns that have no missing values
        if missing_count == 0:
            changes[column] = 0
            continue

        if strategy in {"mean", "median"}:
            # Mean and median require numeric values
            if not pd.api.types.is_numeric_dtype(cleaned_df[column]):
                raise ValueError(
                    f"Column '{column}' must be numeric "
                    f"for the {strategy} strategy."
                )

            fill_value = (
                cleaned_df[column].mean()
                if strategy == "mean"
                else cleaned_df[column].median()
            )

        elif strategy == "mode":
            # Use the most common value
            modes = cleaned_df[column].mode(dropna=True)

            if modes.empty:
                raise ValueError(
                    f"Cannot find a mode for '{column}'."
                )

            fill_value = modes.iloc[0]

        else:
            # Use a clear label for missing values
            fill_value = "Unknown"

        cleaned_df[column] = cleaned_df[column].fillna(fill_value)
        changes[column] = missing_count

    return cleaned_df, {
        "strategy": strategy,
        "filled_values": changes,
    }
