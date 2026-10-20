"""Natural-language query agent."""

import pandas as pd


def query_agent_node(state: dict) -> dict:
    # Read the dataset
    df = pd.read_csv(state["dataset_path"])

    # Read the user's question
    question = state.get("user_question", "").lower()

    # Store the calculation results
    results = []

    # Calculate total revenue
    if "revenue" in question and any(
        word in question for word in ["total", "sum"]
    ):
        total = float(df["revenue"].sum())

        results.append({
            "metric": "total_revenue",
            "value": round(total, 2)
        })

    # Calculate average profit
    if "profit" in question and any(
        word in question for word in ["average", "mean"]
    ):
        average = float(df["profit"].mean())

        results.append({
            "metric": "average_profit",
            "value": round(average, 2)
        })

    # Save the results in the shared state
    return {
        "current_agent": "query_agent",
        "tool_results": state.get("tool_results", []) + results,
        "agent_trace": state.get("agent_trace", []) + [
            {
                "agent": "query_agent",
                "results_count": len(results)
            }
        ]
    }
