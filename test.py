
from pathlib import Path

from src.graph.workflow import build_workflow


def main():
    dataset_path = Path("data/sample/sales.csv.csv")

    if not dataset_path.exists():
        raise FileNotFoundError(
            f"Sample dataset not found: {dataset_path.resolve()}"
        )

    app = build_workflow()

    initial_state = {
        "user_question": (
            "Calculate total revenue, compare revenue by region, "
            "and show a chart."
        ),
        "dataset_path": str(dataset_path),
        "agent_trace": [],
        "tool_results": [],
        "findings": [],
        "charts": [],
        "business_insights": [],
        "errors": [],
        "retry_count": 0,
    }

    print("\nRunning complete Data Analyst Agent workflow...")
    result = app.invoke(initial_state)

    print("\n" + "=" * 55)
    print("WORKFLOW TEST RESULTS")
    print("=" * 55)

    print("\nVerification:", result.get("verification_status"))
    print("Selected agents:", result.get("next_agents"))
    print("Final answer:", result.get("final_answer", "Not generated"))
    print("Charts generated:", len(result.get("charts", [])))
    print("Business insights:", result.get("business_insights", []))
    print("Report path:", result.get("report_path", "Not generated"))
    print("Errors:", result.get("errors", []))

    print("\nAgent execution trace:")
    for item in result.get("agent_trace", []):
        print(item)

    assert result.get("verification_status") == "passed", (
        "Critic verification did not pass."
    )
    assert result.get("final_answer"), "Final answer was not generated."
    assert result.get("charts"), "No charts were generated."
    assert result.get("report_path"), "Report was not generated."

    report_path = Path(result["report_path"])
    assert report_path.exists(), (
        f"Report file does not exist: {report_path}"
    )

    print("\nEND-TO-END WORKFLOW TEST PASSED!")


if __name__ == "__main__":
    main()
