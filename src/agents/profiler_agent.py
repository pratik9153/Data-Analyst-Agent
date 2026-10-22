"""Dataset profiling agent."""

import pandas as pd

from src.tools.data_profiler import profile_data


def profiler_agent_node(state: dict) -> dict:
    # Load the dataset
    df = pd.read_csv(state["dataset_path"])

    # Get information about the dataset
    profile = profile_data(df)

    # Save the profile in the shared state
    return {
        "current_agent": "profiler_agent",
        "dataset_summary": profile,
        "column_names": profile["column_names"],
        "agent_trace": state.get("agent_trace", []) + [
            {
                "agent": "profiler_agent",
                "rows": profile["total_rows"],
                "columns": profile["total_columns"],
                "missing_values": sum(
                    profile["missing_values"].values()
                ),
            }
        ],
    }
