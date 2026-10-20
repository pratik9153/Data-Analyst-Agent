
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
    "business_insights": [],
    "verification_feedback": [],
})

print("Selected agents:", result["next_agents"])
print("Calculated results:", result.get("tool_results", []))
print("Charts generated:", len(result.get("charts", [])))
print("Verification:", result.get("verification_status"))

print("\nBusiness insights:")
for insight in result.get("business_insights", []):
    print("-", insight)

print("\nExecution trace:")
for item in result["agent_trace"]:
    print(item)
