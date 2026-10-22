
"""Plotly chart creation tools."""

import pandas as pd
import plotly.express as px


def create_chart(
    df: pd.DataFrame,
    chart_type: str,
    x_column: str,
    y_column: str,
    title: str | None = None,
) -> dict:
    # Check that the requested columns exist
    for column in [x_column, y_column]:
        if column not in df.columns:
            raise ValueError(f"Column not found: {column}")

    # Check the requested chart type
    chart_type = chart_type.lower().strip()

    if chart_type not in {"bar", "line", "scatter"}:
        raise ValueError(
            "chart_type must be 'bar', 'line', or 'scatter'."
        )

    # Keep only the columns needed for the chart
    chart_df = df[[x_column, y_column]].copy()

    # Convert values to numbers for the y-axis
    chart_df[y_column] = pd.to_numeric(
        chart_df[y_column],
        errors="coerce",
    )

    # Remove rows that cannot be plotted
    chart_df = chart_df.dropna(subset=[x_column, y_column])

    if chart_df.empty:
        raise ValueError(
            "No valid rows are available for this chart."
        )

    # Create the requested chart
    chart_title = title or f"{y_column} by {x_column}"

    if chart_type == "bar":
        fig = px.bar(
            chart_df,
            x=x_column,
            y=y_column,
            title=chart_title,
        )
    elif chart_type == "line":
        fig = px.line(
            chart_df,
            x=x_column,
            y=y_column,
            title=chart_title,
        )
    else:
        fig = px.scatter(
            chart_df,
            x=x_column,
            y=y_column,
            title=chart_title,
        )

    # Return a serializable chart specification
    return {
        "title": chart_title,
        "chart_type": chart_type,
        "x_column": x_column,
        "y_column": y_column,
        "figure_json": fig.to_json(),
        "rows_plotted": len(chart_df),
    }
