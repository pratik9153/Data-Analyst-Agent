"""Conditional agent routing."""

def route_agents(state: dict) -> str:
    # Get the agents selected by the supervisor
    next_agents = state.get("next_agents", [])

    # Send the workflow to the first selected agent
    if next_agents:
        return next_agents[0]

    # Use the profiler if no agent was selected
    return "data_profiler"
