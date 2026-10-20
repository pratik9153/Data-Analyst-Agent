
from langgraph.graph import StateGraph, START, END

from src.graph.state import DataAnalystState
from src.graph.nodes import supervisor_node

from src.agents.query_agent import query_agent_node
from src.agents.analysis_agent import analysis_agent_node
from src.agents.visualization_agent import visualization_agent_node
from src.agents.critic_agent import critic_agent_node
from src.agents.business_analyst_agent import business_analyst_node


# Specialist agents that the supervisor can select
AGENT_NAMES = [
    "query_agent",
    "analysis_agent",
    "visualization_agent",
]


def build_workflow():
    # Create the graph using our shared state
    graph = StateGraph(DataAnalystState)

    # Register all nodes
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("query_agent", query_agent_node)
    graph.add_node("analysis_agent", analysis_agent_node)
    graph.add_node("visualization_agent", visualization_agent_node)
    graph.add_node("critic_agent", critic_agent_node)
    graph.add_node("business_analyst", business_analyst_node)

    # Start with the supervisor
    graph.add_edge(START, "supervisor")

    # Select the first agent chosen by the supervisor
    def first_agent(state: DataAnalystState) -> str:
        agents = state.get("next_agents", [])
        return agents[0] if agents else "critic_agent"

    # Select the next agent that has not run yet
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

    # Route from the supervisor to the first selected agent
    graph.add_conditional_edges(
        "supervisor",
        first_agent,
        {
            "query_agent": "query_agent",
            "analysis_agent": "analysis_agent",
            "visualization_agent": "visualization_agent",
            "critic_agent": "critic_agent",
        },
    )

    # Run selected specialist agents in sequence
    for agent_name in AGENT_NAMES:
        graph.add_conditional_edges(
            agent_name,
            next_agent,
            {
                "query_agent": "query_agent",
                "analysis_agent": "analysis_agent",
                "visualization_agent": "visualization_agent",
                "critic_agent": "critic_agent",
            },
        )

    # Run the business analyst only when verification passes
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

    # Finish after business insights are generated
    graph.add_edge("business_analyst", END)

    return graph.compile()
