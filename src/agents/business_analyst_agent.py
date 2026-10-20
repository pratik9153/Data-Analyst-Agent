"""Business insights agent."""

def business_analyst_node(state: dict) -> dict:
    # Collect the verified findings
    findings = state.get("findings", [])
    insights = []

    # Stop if verification has failed
    if state.get("verification_status") != "passed":
        return {
            "current_agent": "business_analyst",
            "business_insights": [
                "Insights were not generated because verification failed."
            ],
            "agent_trace": state.get("agent_trace", []) + [
                {
                    "agent": "business_analyst",
                    "status": "skipped"
                }
            ]
        }

    # Explain regional revenue
    for finding in findings:
        if finding.get("analysis") == "revenue_by_region":
            values = finding.get("result", {})

            # Ignore missing-region labels when comparing real regions
            valid_values = {
                name: value
                for name, value in values.items()
                if name.lower() not in {"nan", "none", "missing region"}
            }

            if valid_values:
                top_region = max(valid_values, key=valid_values.get)

                insights.append(
                    f"{top_region} has the highest recorded regional "
                    f"revenue at {valid_values[top_region]:,.2f}."
                )

        # Explain category profit
        if finding.get("analysis") == "profit_by_category":
            values = finding.get("result", {})

            if values:
                top_category = max(values, key=values.get)

                insights.append(
                    f"{top_category} has the highest recorded category "
                    f"profit at {values[top_category]:,.2f}."
                )

    if not insights:
        insights.append(
            "No supported business insights could be generated "
            "from the available findings."
        )

    return {
        "current_agent": "business_analyst",
        "business_insights": insights,
        "agent_trace": state.get("agent_trace", []) + [
            {
                "agent": "business_analyst",
                "insights_count": len(insights)
            }
        ]
    }
