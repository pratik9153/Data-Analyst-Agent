"""CSV loading and validation."""

import pandas as pd
from pathlib import Path


def load_data(file_path: str) -> pd.DataFrame:
    # Check whether the file exists
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    # Make sure the file is a CSV
    if path.suffix.lower() != ".csv":
        raise ValueError("Please provide a CSV file.")

    # Load the dataset
    df = pd.read_csv(path)

    # Reject empty datasets
    if df.empty:
        raise ValueError("The uploaded CSV file is empty.")

    return df
