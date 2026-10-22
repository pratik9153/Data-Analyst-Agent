
"""Analysis agent for comparisons and statistical findings."""

from src.tools.data_loader import load_data
from src.tools.query_tools import group_metric
from src.tools.statistical_tools import describe_column


def analysis_agent_node(state: dict) -> dict:
    # Load the dataset using the shared loader
    df = load_data(state["dataset_path"])

    # Store the findings produced by this agent
    findings = []

    # Compare revenue across regions
    if "region" in df.columns and "revenue" in df.columns:
        result = group_metric(
            df=df,
            group_by="region",
            column="revenue",
            operation="sum",
        )

        # Sort regions by revenue, from highest to lowest
        sorted_revenue = dict(
            sorted(
                result["results"].items(),
                key=lambda item: item[1],
                reverse=True,
            )
        )

        findings.append({
            "analysis": "revenue_by_region",
            "result": sorted_revenue,
        })

    # Compare profit across product categories
    if "category" in df.columns and "profit" in df.columns:
        result = group_metric(
            df=df,
            group_by="category",
            column="profit",
            operation="sum",
        )

        # Sort categories by profit, from highest to lowest
        sorted_profit = dict(
            sorted(
                result["results"].items(),
                key=lambda item: item[1],
                reverse=True,
            )
        )

        findings.append({
            "analysis": "profit_by_category",
            "result": sorted_profit,
        })

    # Add descriptive statistics when the question requests them
    question = state.get("user_question", "").lower()

    if any(
        word in question
        for word in ["statistics", "distribution", "standard deviation"]
    ):
        for column in ["revenue", "profit"]:
            if column in df.columns:
                findings.append({
                    "analysis": f"{column}_statistics",
                    "result": describe_column(df, column),
                })

    # Save the findings in the shared workflow state
    return {
        "current_agent": "analysis_agent",
        "findings": state.get("findings", []) + findings,
        "agent_trace": state.get("agent_trace", []) + [
            {
                "agent": "analysis_agent",
                "findings_count": len(findings),
            }
        ],
    }
