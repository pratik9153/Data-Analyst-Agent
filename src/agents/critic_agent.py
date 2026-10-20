"""Result verification agent."""

import math


def critic_agent_node(state: dict) -> dict:
    # Collect any problems found during verification
    feedback = []

    # Check calculated results
    for item in state.get("tool_results", []):
        value = item.get("value")

        if not isinstance(value, (int, float)):
            feedback.append(
                f"Invalid numeric result: {item.get('metric')}"
            )
        elif not math.isfinite(value):
            feedback.append(
                f"Non-finite result: {item.get('metric')}"
            )

    # Check analysis findings
    for finding in state.get("findings", []):
        if not finding.get("analysis"):
            feedback.append("An analysis finding has no name.")

        if not isinstance(finding.get("result"), dict):
            feedback.append(
                f"Invalid result structure: {finding.get('analysis')}"
            )

    # Set the verification status
    status = "passed" if not feedback else "failed"

    # Save the verification outcome
    return {
        "current_agent": "critic_agent",
        "verification_status": status,
        "verification_feedback": feedback,
        "agent_trace": state.get("agent_trace", []) + [
            {
                "agent": "critic_agent",
                "status": status,
                "issues_found": len(feedback)
            }
        ]
    }
