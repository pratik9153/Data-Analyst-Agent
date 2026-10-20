
def supervisor_node(state: dict) -> dict:
    # Read the user's question
    question = state.get("user_question", "").lower().strip()

    next_agents = []

    # Select the profiler for dataset and data-quality questions
    profile_keywords = [
        "dataset",
        "columns",
        "column",
        "rows",
        "missing",
        "duplicates",
        "duplicate",
        "profile",
        "quality",
        "data types",
        "datatypes",
        "null",
        "empty",
    ]

    if any(word in question for word in profile_keywords):
        next_agents.append("data_profiler")

    # Select the query agent for numerical calculations
    query_keywords = [
        "total",
        "sum",
        "average",
        "mean",
        "count",
        "maximum",
        "minimum",
        "highest",
        "lowest",
        "revenue",
        "profit",
        "sales",
        "how many",
        "how much",
    ]

    if any(word in question for word in query_keywords):
        next_agents.append("query_agent")

    # Select the analysis agent for comparisons and patterns
    analysis_keywords = [
        "analyze",
        "analyse",
        "analysis",
        "trend",
        "insight",
        "region",
        "category",
        "compare",
        "comparison",
        "recommend",
        "recommendation",
        "pattern",
        "performance",
        "why",
    ]

    if any(word in question for word in analysis_keywords):
        next_agents.append("analysis_agent")

    # Select the visualization agent when a chart is requested
    visualization_keywords = [
        "chart",
        "charts",
        "plot",
        "visualize",
        "visualise",
        "visualization",
        "visualisation",
        "graph",
        "bar chart",
        "line chart",
        "pie chart",
    ]

    if any(word in question for word in visualization_keywords):
        next_agents.append("visualization_agent")

    # Use the profiler when no specific agent matches
    if not next_agents:
        next_agents.append("data_profiler")

    # Remove duplicate selections while preserving their order
    next_agents = list(dict.fromkeys(next_agents))

    # Record the supervisor's decision
    return {
        "next_agents": next_agents,
        "current_agent": "supervisor",
        "agent_trace": state.get("agent_trace", []) + [
            {
                "agent": "supervisor",
                "decision": next_agents,
            }
        ],
    }
