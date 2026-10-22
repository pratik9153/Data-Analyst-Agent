
from langgraph.graph import StateGraph, START, END

from src.graph.state import DataAnalystState
from src.graph.nodes import supervisor_node

from src.agents.profiler_agent import profiler_agent_node
from src.agents.query_agent import query_agent_node
from src.agents.analysis_agent import analysis_agent_node
from src.agents.visualization_agent import visualization_agent_node
from src.agents.critic_agent import critic_agent_node
from src.agents.business_analyst_agent import business_analyst_node
from src.agents.reporting_agent import reporting_agent_node



# Specialist agents the supervisor can select
AGENT_NAMES = [
    "profiler_agent",
    "query_agent",
    "analysis_agent",
    "visualization_agent",
]


def build_workflow():
    # Create the graph using our shared state
    graph = StateGraph(DataAnalystState)

    # Register all agents
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("profiler_agent", profiler_agent_node)
    graph.add_node("query_agent", query_agent_node)
    graph.add_node("analysis_agent", analysis_agent_node)
    graph.add_node("visualization_agent", visualization_agent_node)
    graph.add_node("critic_agent", critic_agent_node)
    graph.add_node("business_analyst", business_analyst_node)
    graph.add_node("reporting_agent", reporting_agent_node)

    # Start with the supervisor
    graph.add_edge(START, "supervisor")

    # Choose the first agent selected by the supervisor
    def first_agent(state: DataAnalystState) -> str:
        agents = state.get("next_agents", [])
        return agents[0] if agents else "critic_agent"

    # Find the next selected agent that has not run yet
    def next_agent(state: DataAnalystState) -> str:
        agents = state.get("next_agents", [])

        completed = {
            item["agent"]
            for item in state.get("agent_trace", [])
        }

        remaining = [
            agent
            for agent in agents
            if agent in AGENT_NAMES and agent not in completed
        ]

        return remaining[0] if remaining else "critic_agent"

    # Map valid routes between agents
    specialist_routes = {
        "profiler_agent": "profiler_agent",
        "query_agent": "query_agent",
        "analysis_agent": "analysis_agent",
        "visualization_agent": "visualization_agent",
        "critic_agent": "critic_agent",
    }

    # Route from the supervisor to the first selected agent
    graph.add_conditional_edges(
        "supervisor",
        first_agent,
        specialist_routes,
    )

    # Run selected specialist agents in sequence
    for agent_name in AGENT_NAMES:
        graph.add_conditional_edges(
            agent_name,
            next_agent,
            specialist_routes,
        )

    # Continue only when verification passes
    def after_critic(state: DataAnalystState) -> str:
        if state.get("verification_status") == "passed":
            return "business_analyst"

        return END

    graph.add_conditional_edges(
        "critic_agent",
        after_critic,
        {
            "business_analyst": "business_analyst",
            END: END,
        },
    )

    # Generate the final answer
    graph.add_edge("business_analyst", "reporting_agent")
    graph.add_edge("reporting_agent", END)

    return graph.compile()
