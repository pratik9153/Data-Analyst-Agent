
"""Routes user questions to the required specialist agents."""

import json
import logging
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

logger = logging.getLogger(__name__)

AVAILABLE_AGENTS = [
    "profiler_agent",
    "query_agent",
    "analysis_agent",
    "visualization_agent",
]

client = None

if os.getenv("OPENAI_API_KEY"):
    client = OpenAI()


def _keyword_routing(question: str) -> list[str]:
    """Fallback routing using simple keyword matching."""

    question = question.lower()
    next_agents = []

    profile_keywords = [
        "dataset", "columns", "column", "rows",
        "missing", "duplicates", "duplicate",
        "profile", "quality", "data types",
        "datatypes", "null", "empty",
    ]

    query_keywords = [
        "total", "sum", "average", "mean", "count",
        "maximum", "minimum", "highest", "lowest",
        "revenue", "profit", "sales", "how many",
        "how much",
    ]

    analysis_keywords = [
        "analyze", "analyse", "analysis", "trend",
        "insight", "region", "category", "compare",
        "comparison", "recommend", "recommendation",
        "pattern", "performance", "why",
    ]

    visualization_keywords = [
        "chart", "charts", "plot", "visualize",
        "visualise", "visualization", "visualisation",
        "graph", "bar chart", "line chart", "pie chart",
    ]

    if any(word in question for word in profile_keywords):
        next_agents.append("profiler_agent")

    if any(word in question for word in query_keywords):
        next_agents.append("query_agent")

    if any(word in question for word in analysis_keywords):
        next_agents.append("analysis_agent")

    if any(word in question for word in visualization_keywords):
        next_agents.append("visualization_agent")

    return next_agents or ["profiler_agent"]


def _openai_routing(question: str) -> list[str]:
    """Use OpenAI to identify the specialist agents required."""

    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        instructions=(
            "You route questions for a CSV Data Analyst Agent. "
            "Select only the necessary agents from this list: "
            "profiler_agent, query_agent, analysis_agent, "
            "visualization_agent. "
            "Use profiler_agent for dataset structure and data quality; "
            "query_agent for calculations; analysis_agent for comparisons, "
            "patterns and insights; visualization_agent for chart requests. "
            "A question may need multiple agents. "
            "Return only JSON with this format: "
            '{"next_agents": ["query_agent", "analysis_agent"]}'
        ),
        input=question,
    )

    result = json.loads(response.output_text)
    agents = result.get("next_agents", [])

    if not isinstance(agents, list):
        raise ValueError("OpenAI returned an invalid agent list.")

    # Only allow agents that exist in our project.
    agents = [
        agent for agent in agents
        if agent in AVAILABLE_AGENTS
    ]

    if not agents:
        raise ValueError("OpenAI did not select a valid agent.")

    return list(dict.fromkeys(agents))


def supervisor_node(state: dict) -> dict:
    """Select specialist agents and record the routing decision."""

    question = state.get("user_question", "").strip()
    next_agents = None
    routing_method = "keyword_fallback"

    if question and client is not None:
        try:
            next_agents = _openai_routing(question)
            routing_method = "openai"
        except Exception:
            logger.exception(
                "OpenAI routing failed; using keyword routing."
            )

    if next_agents is None:
        next_agents = _keyword_routing(question)

    trace = state.get("agent_trace", []) + [
        {
            "agent": "supervisor",
            "decision": next_agents,
            "routing_method": routing_method,
        }
    ]

    return {
        "next_agents": next_agents,
        "current_agent": "supervisor",
        "agent_trace": trace,
    }
