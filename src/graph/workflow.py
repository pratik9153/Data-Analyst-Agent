
from langgraph.graph import StateGraph, START, END

from src.graph.state import DataAnalystState
from src.graph.nodes import supervisor_node
from src.agents.query_agent import query_agent_node
from src.agents.analysis_agent import analysis_agent_node
from src.agents.visualization_agent import visualization_agent_node


def build_workflow():
    # Create the graph using our shared state
    graph = StateGraph(DataAnalystState)

    # Register the agents
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("query_agent", query_agent_node)
    graph.add_node("analysis_agent", analysis_agent_node)
    graph.add_node("visualization_agent", visualization_agent_node)

    # Start with the supervisor
    graph.add_edge(START, "supervisor")

    # Select the first agent chosen by the supervisor
    def first_agent(state: DataAnalystState) -> str:
        agents = state.get("next_agents", [])
        return agents[0] if agents else END

    # Select the next agent that has not run yet
    def next_agent(state: DataAnalystState) -> str:
        agents = state.get("next_agents", [])

        completed = {
            item["agent"]
            for item in state.get("agent_trace", [])
        }

        remaining = [
            agent for agent in agents
            if agent not in completed
        ]

        return remaining[0] if remaining else END

    graph.add_conditional_edges(
        "supervisor",
        first_agent,
        {
            "query_agent": "query_agent",
            "analysis_agent": "analysis_agent",
            "visualization_agent": "visualization_agent",
            END: END,
        },
    )

    # Continue through any other selected agents
    for agent_name in [
        "query_agent",
        "analysis_agent",
        "visualization_agent",
    ]:
        graph.add_conditional_edges(
            agent_name,
            next_agent,
            {
                "query_agent": "query_agent",
                "analysis_agent": "analysis_agent",
                "visualization_agent": "visualization_agent",
                END: END,
            },
        )

    return graph.compile()
