"""Data profiling calculations."""


import pandas as pd


def profile_data(df: pd.DataFrame) -> dict:
    # Get the number of rows and columns
    rows, columns = df.shape

    # Count missing values in each column
    missing_values = df.isnull().sum().to_dict()

    # Count duplicate rows
    duplicate_rows = int(df.duplicated().sum())

    # Get the data type of each column
    data_types = df.dtypes.astype(str).to_dict()

    # Get basic statistics for numeric columns
    numeric_summary = df.describe().to_dict()

    # Return the dataset information
    return {
        "total_rows": rows,
        "total_columns": columns,
        "column_names": df.columns.tolist(),
        "data_types": data_types,
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "numeric_summary": numeric_summary,
    }

