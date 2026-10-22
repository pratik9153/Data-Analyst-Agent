
"""Result verification agent."""

from src.tools.data_loader import load_data
from src.tools.verification_tools import verify_metric


def critic_agent_node(state: dict) -> dict:
    # Collect any problems found during verification
    feedback = []

    # Load the original dataset for independent checks
    df = load_data(state["dataset_path"])

    # Verify each calculated metric
    for item in state.get("tool_results", []):
        metric = item.get("metric", "")
        column = item.get("column")
        operation = item.get("operation")
        value = item.get("value")

        # Older results may not include column and operation
        if not column or not operation:
            feedback.append(
                f"Cannot independently verify metric '{metric}': "
                "column or operation is missing."
            )
            continue

        result = verify_metric(
            df=df,
            column=column,
            operation=operation,
            reported_value=value,
        )

        if not result["passed"]:
            feedback.append(
                f"Verification failed for '{metric}': "
                f"{result['reason']}"
            )

    # Check the structure of analysis findings
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
                "issues_found": len(feedback),
            }
        ],
    }
