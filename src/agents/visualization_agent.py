
"""Visualization agent."""

from src.tools.data_loader import load_data
from src.tools.chart_tools import create_chart


def visualization_agent_node(state: dict) -> dict:
    # Load the dataset
    df = load_data(state["dataset_path"])

    charts = []

    # Create a revenue chart by region
    if "region" in df.columns and "revenue" in df.columns:
        chart = create_chart(
            df=df,
            chart_type="bar",
            x_column="region",
            y_column="revenue",
            title="Revenue by Region",
        )

        charts.append({
            "chart_name": "revenue_by_region",
            "chart_type": chart["chart_type"],
            "title": chart["title"],
            "figure_json": chart["figure_json"],
        })

    # Create a profit chart by category
    if "category" in df.columns and "profit" in df.columns:
        chart = create_chart(
            df=df,
            chart_type="bar",
            x_column="category",
            y_column="profit",
            title="Profit by Category",
        )

        charts.append({
            "chart_name": "profit_by_category",
            "chart_type": chart["chart_type"],
            "title": chart["title"],
            "figure_json": chart["figure_json"],
        })

    # Save chart specifications in the shared state
    return {
        "current_agent": "visualization_agent",
        "charts": state.get("charts", []) + charts,
        "agent_trace": state.get("agent_trace", []) + [
            {
                "agent": "visualization_agent",
                "charts_count": len(charts),
            }
        ],
    }
