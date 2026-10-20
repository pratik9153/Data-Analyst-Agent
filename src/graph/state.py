"""Shared workflow state."""

from typing import Any, TypedDict


class DataAnalystState(TypedDict, total=False):
    # Question asked by the user and path of the dataset
    user_question: str
    dataset_path: str

    # Basic information about the dataset
    dataset_summary: dict[str, Any]
    column_names: list[str]

    # Stores which agent should run next
    next_agents: list[str]
    current_agent: str

    # Keeps track of which agents have run
    agent_trace: list[dict[str, Any]]

    # Stores results from tools and agents
    tool_results: list[dict[str, Any]]
    findings: list[dict[str, Any]]
    charts: list[dict[str, Any]]
    business_insights: list[str]

    # Stores the checking result and any feedback
    verification_status: str
    verification_feedback: list[str]

    # Counts retries and stores errors
    retry_count: int
    errors: list[str]

    # Stores the final answer and report location
    final_answer: str
    report_path: str
