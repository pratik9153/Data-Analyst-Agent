
from src.graph.workflow import build_workflow

app = build_workflow()

result = app.invoke({
    "dataset_path": "data/sample/sales.csv.csv",
    "user_question": (
        "Calculate total revenue, analyze regional performance, "
        "and create charts"
    ),
    "agent_trace": [],
    "tool_results": [],
    "findings": [],
    "charts": [],
})

print("Selected agents:", result["next_agents"])
print("Calculated results:", result.get("tool_results", []))
print("Analysis findings:", result.get("findings", []))
print("Charts generated:", len(result.get("charts", [])))
print("Execution trace:", result["agent_trace"])
