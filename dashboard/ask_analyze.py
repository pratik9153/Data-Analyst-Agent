
"""Natural-language analysis page connected to LangGraph."""

from pathlib import Path
import tempfile

import pandas as pd
import streamlit as st

from src.graph.workflow import build_workflow
from database.db import initialize_database
from database.repositories import save_analysis


def render_ask_analyze() -> None:
    st.title("Ask & Analyze")
    st.caption(
        "Upload a dataset, ask a business question, and let your "
        "multi-agent workflow analyze it."
    )

    uploaded_file = st.file_uploader(
        "Upload your CSV dataset",
        type=["csv"],
        key="analysis_upload",
    )

    if uploaded_file is None:
        # Reuse a dataset already uploaded in Data Explorer.
        df = st.session_state.get("uploaded_df")
        dataset_name = st.session_state.get("uploaded_dataset_name")

        if df is None:
            st.info("Upload a CSV file to begin your analysis.")
            return

        st.success(f"Using uploaded dataset: {dataset_name}")
    else:
        try:
            df = pd.read_csv(uploaded_file)
            dataset_name = uploaded_file.name

            if df.empty:
                st.warning("The uploaded CSV contains no data rows.")
                return

            st.session_state["uploaded_df"] = df
            st.session_state["uploaded_dataset_name"] = dataset_name

        except (ValueError, UnicodeDecodeError, pd.errors.ParserError) as error:
            st.error(f"Could not read the CSV file: {error}")
            return

    st.write(
        f"**Dataset:** {dataset_name} · "
        f"**Rows:** {len(df):,} · "
        f"**Columns:** {len(df.columns):,}"
    )

    question = st.text_area(
        "What would you like to know?",
        placeholder=(
            "Example: Calculate total revenue, analyze regional "
            "performance, and create charts."
        ),
        height=100,
        key="analysis_question",
    )

    if st.button("Run Analysis", type="primary", use_container_width=True):
        if not question.strip():
            st.warning("Please enter a question first.")
            return

        # Save the uploaded data to a temporary CSV so the existing
        # workflow can read it using its dataset_path field.
        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".csv",
                encoding="utf-8",
                newline="",
                delete=False,
            ) as temp_file:
                temp_path = Path(temp_file.name)
                df.to_csv(temp_path, index=False)

            initial_state = {
                "dataset_path": str(temp_path),
                "user_question": question.strip(),
                "dataset_summary": {},
                "column_names": [],
                "next_agents": [],
                "current_agent": "",
                "agent_trace": [],
                "tool_results": [],
                "findings": [],
                "charts": [],
                "business_insights": [],
                "verification_status": "",
                "verification_feedback": [],
                "retry_count": 0,
                "errors": [],
                "final_answer": "",
                "report_path": "",
            }

            with st.spinner("Your analysis agents are working..."):
                workflow = build_workflow()
                result = workflow.invoke(initial_state)

            st.session_state["latest_analysis_result"] = result

            st.success("Analysis workflow finished.")

            # Save the result in SQLite.
            try:
                initialize_database()

                analysis_id = save_analysis(
                    dataset_name=str(dataset_name),
                    user_question=question.strip(),
                    verification_status=(
                        result.get("verification_status") or "unknown"
                    ),
                    report_path=result.get("report_path"),
                    final_answer=result.get("final_answer"),
                )

                st.session_state["latest_analysis_id"] = analysis_id
                st.success(f"Analysis history saved. ID: {analysis_id}")

            except Exception as db_error:
                st.warning(
                    "The analysis completed, but saving its history "
                    f"failed: {db_error}"
                )

        except Exception as error:
            st.error(f"Analysis failed: {error}")

        finally:
            # The workflow and report generation have finished using
            # the temporary dataset path.
            if temp_path is not None:
                try:
                    temp_path.unlink(missing_ok=True)
                except OSError:
                    pass

    # Show the most recent result, including after Streamlit reruns.
    result = st.session_state.get("latest_analysis_result")

    if result:
        st.divider()
        st.subheader("Analysis Results")

        status = result.get("verification_status", "unknown")
        if status == "passed":
            st.success("Critic verification passed.")
        else:
            st.warning(f"Verification status: {status}")

        st.markdown("### Final Answer")
        st.markdown(result.get("final_answer") or "No final answer available.")

        feedback = result.get("verification_feedback", [])
        if feedback:
            st.markdown("### Verification Feedback")
            for item in feedback:
                st.write(f"- {item}")

        insights = result.get("business_insights", [])
        if insights:
            st.markdown("### Business Insights")
            for insight in insights:
                st.write(f"- {insight}")

        charts = result.get("charts", [])
        if charts:
            st.markdown("### Generated Charts")

            for chart in charts:
                figure_json = chart.get("figure_json")

                if figure_json:
                    try:
                        import plotly.io as pio

                        figure = pio.from_json(figure_json)
                        st.plotly_chart(
                            figure,
                            use_container_width=True,
                        )
                    except (ValueError, TypeError) as chart_error:
                        st.warning(
                            f"Could not display {chart.get('title', 'chart')}: "
                            f"{chart_error}"
                        )
                else:
                    st.write(chart.get("title", "Chart"))

        with st.expander("Agent Execution Trace"):
            st.json(result.get("agent_trace", []))

        report_path = result.get("report_path")

        if report_path and Path(report_path).is_file():
            with open(report_path, "rb") as report_file:
                st.download_button(
                    "Download Markdown Report",
                    data=report_file.read(),
                    file_name=Path(report_path).name,
                    mime="text/markdown",
                )
