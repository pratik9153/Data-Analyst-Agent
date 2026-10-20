
import pandas as pd


def analysis_agent_node(state: dict) -> dict:
    # Load the dataset
    df = pd.read_csv(state["dataset_path"])

    findings = []

    # Compare revenue across regions
    if "region" in df.columns and "revenue" in df.columns:
        region_revenue = (
            df.groupby("region", dropna=False)["revenue"]
            .sum()
            .sort_values(ascending=False)
        )

        findings.append({
            "analysis": "revenue_by_region",
            "result": {
                str(region): round(float(value), 2)
                for region, value in region_revenue.items()
            }
        })

    # Compare profit across categories
    if "category" in df.columns and "profit" in df.columns:
        category_profit = (
            df.groupby("category", dropna=False)["profit"]
            .sum()
            .sort_values(ascending=False)
        )

        findings.append({
            "analysis": "profit_by_category",
            "result": {
                str(category): round(float(value), 2)
                for category, value in category_profit.items()
            }
        })

    # Save the findings
    return {
        "current_agent": "analysis_agent",
        "findings": state.get("findings", []) + findings,
        "agent_trace": state.get("agent_trace", []) + [
            {
                "agent": "analysis_agent",
                "findings_count": len(findings)
            }
        ]
    }
