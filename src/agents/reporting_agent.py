
"""Reporting agent for final answers and report export."""

from src.tools.report_tools import export_markdown_report


def reporting_agent_node(state: dict) -> dict:
    # Collect results from the other agents
    dataset_summary = state.get("dataset_summary", {})
    tool_results = state.get("tool_results", [])
    findings = state.get("findings", [])
    insights = state.get("business_insights", [])
    charts = state.get("charts", [])

    sections = []

    # Do not present results as verified if verification failed
    if state.get("verification_status") != "passed":
        feedback = state.get("verification_feedback", [])

        answer = (
            "The results could not be verified. "
            "Please review the verification feedback before using them."
        )

        if feedback:
            answer += "\n\nVerification feedback:\n"
            answer += "\n".join(f"- {item}" for item in feedback)

    else:
        # Add dataset profiling information
        if dataset_summary:
            sections.append("Dataset Profile:")
            sections.append(
                f"- Total rows: "
                f"{dataset_summary.get('total_rows', 'Unavailable')}"
            )
            sections.append(
                f"- Total columns: "
                f"{dataset_summary.get('total_columns', 'Unavailable')}"
            )

            column_names = dataset_summary.get("column_names", [])
            sections.append(f"- Column names: {', '.join(column_names)}")

            sections.append(
                f"- Duplicate rows: "
                f"{dataset_summary.get('duplicate_rows', 'Unavailable')}"
            )

            # Include only columns that contain missing values
            missing_values = dataset_summary.get("missing_values", {})
            missing_columns = {
                column: count
                for column, count in missing_values.items()
                if count > 0
            }

            sections.append("- Missing values:")

            if missing_columns:
                for column, count in missing_columns.items():
                    sections.append(f"  - {column}: {count}")
            else:
                sections.append("  - None")

            # Include column data types
            data_types = dataset_summary.get("data_types", {})

            if data_types:
                sections.append("- Data types:")

                for column, data_type in data_types.items():
                    sections.append(f"  - {column}: {data_type}")

        # Add calculated results
        if tool_results:
            sections.append("\nCalculated Results:")

            for item in tool_results:
                metric = item.get("metric", "Unknown metric")
                value = item.get("value", "Unavailable")
                sections.append(f"- {metric}: {value}")

        # Add analysis findings
        if findings:
            sections.append("\nAnalysis Findings:")

            for item in findings:
                name = item.get("analysis", "Analysis")
                result = item.get("result", {})
                sections.append(f"- {name}:")

                if isinstance(result, dict):
                    for label, value in result.items():
                        sections.append(f"  - {label}: {value}")
                else:
                    sections.append(f"  - {result}")

        # Add business insights
        if insights:
            sections.append("\nBusiness Insights:")

            for insight in insights:
                sections.append(f"- {insight}")

        # Add generated chart information
        if charts:
            sections.append(f"\nCharts generated: {len(charts)}")

            for chart in charts:
                title = chart.get("title", "Untitled chart")
                sections.append(f"- {title}")

        # Build the final answer
        answer = "\n".join(sections)

        if not answer.strip():
            answer = "No results were produced for this question."

    # Export the final answer, including verification feedback if applicable
    report_path = None
    report_error = None

    try:
        report_result = export_markdown_report(
            title="Data Analyst Agent Report",
            content=answer,
            output_dir="reports",
        )
        report_path = report_result["report_path"]

    except Exception as error:
        # Report export failure should not hide the final answer
        report_error = str(error)

    # Update the shared workflow state
    trace_entry = {
        "agent": "reporting_agent",
        "status": "completed",
        "report_path": report_path,
    }

    if report_error:
        trace_entry["report_error"] = report_error

    return {
        "current_agent": "reporting_agent",
        "final_answer": answer,
        "report_path": report_path,
        "errors": state.get("errors", [])
        + ([f"Report export failed: {report_error}"] if report_error else []),
        "agent_trace": state.get("agent_trace", []) + [trace_entry],
    }
