
"""Query agent for dataset calculations."""

from src.tools.data_loader import load_data
from src.tools.query_tools import calculate_metric


def query_agent_node(state: dict) -> dict:
    # Load the dataset
    df = load_data(state["dataset_path"])

    # Read the user's question
    question = state.get("user_question", "").lower()

    results = []

    # Define the calculations supported by this agent
    calculations = [
        {
            "column": "revenue",
            "keywords": ["revenue"],
            "operations": {
                "total": "sum",
                "sum": "sum",
                "average": "mean",
                "mean": "mean",
            },
        },
        {
            "column": "profit",
            "keywords": ["profit"],
            "operations": {
                "total": "sum",
                "sum": "sum",
                "average": "mean",
                "mean": "mean",
            },
        },
    ]

    # Match the question with the available calculations
    for calculation in calculations:
        column = calculation["column"]

        if column not in df.columns:
            continue

        if not any(
            word in question for word in calculation["keywords"]
        ):
            continue

        for keyword, operation in calculation["operations"].items():
            if keyword in question:
                result = calculate_metric(
                    df=df,
                    column=column,
                    operation=operation,
                )

                metric_name = f"{operation}_{column}"

                # Avoid repeating the same calculation
                if any(
                    item["metric"] == metric_name
                    for item in results
                ):
                    continue

                results.append({
                    "metric": metric_name,
                    "value": result["value"],
                    "column": column,
                    "operation": operation,
                })

    # Save the calculated results
    return {
        "current_agent": "query_agent",
        "tool_results": state.get("tool_results", []) + results,
        "agent_trace": state.get("agent_trace", []) + [
            {
                "agent": "query_agent",
                "results_count": len(results),
            }
        ],
    }
