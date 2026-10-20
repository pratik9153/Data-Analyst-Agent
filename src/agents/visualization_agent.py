"""Visualization agent."""

import pandas as pd
import plotly.express as px


def visualization_agent_node(state: dict) -> dict:
    # Load the dataset
    df = pd.read_csv(state["dataset_path"])

    charts = []
    question = state.get("user_question", "").lower()

    # Create a revenue chart by region
    if "region" in df.columns and "revenue" in df.columns:
        region_data = (
            df.groupby("region", dropna=False, as_index=False)["revenue"]
            .sum()
            .sort_values("revenue", ascending=False)
        )

        region_data["region"] = region_data["region"].fillna("Missing region")

        fig = px.bar(
            region_data,
            x="region",
            y="revenue",
            title="Revenue by Region",
            labels={
                "region": "Region",
                "revenue": "Total Revenue"
            }
        )

        charts.append({
            "chart_name": "revenue_by_region",
            "chart_type": "bar",
            "title": "Revenue by Region",
            "figure_json": fig.to_json()
        })

    # Create a profit chart by category
    if "category" in df.columns and "profit" in df.columns:
        category_data = (
            df.groupby("category", as_index=False)["profit"]
            .sum()
            .sort_values("profit", ascending=False)
        )

        fig = px.bar(
            category_data,
            x="category",
            y="profit",
            title="Profit by Category",
            labels={
                "category": "Category",
                "profit": "Total Profit"
            }
        )

        charts.append({
            "chart_name": "profit_by_category",
            "chart_type": "bar",
            "title": "Profit by Category",
            "figure_json": fig.to_json()
        })

    # Save chart specifications in the shared state
    return {
        "current_agent": "visualization_agent",
        "charts": state.get("charts", []) + charts,
        "agent_trace": state.get("agent_trace", []) + [
            {
                "agent": "visualization_agent",
                "charts_count": len(charts)
            }
        ]
    }
