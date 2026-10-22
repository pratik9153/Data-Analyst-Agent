
"""Data Analyst Agent: Streamlit dashboard."""

import json
import os
import tempfile
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# =========================================================
# 1. CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Data Analyst Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp {
        background: #07111f;
        color: #e8f0ff;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1b30, #091323);
        border-right: 1px solid #1b3453;
    }

    [data-testid="stHeader"] {
        background: rgba(7, 17, 31, 0.95);
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1700px;
    }

    h1, h2, h3 {
        color: #f1f6ff;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #101f33, #0b1728);
        border: 1px solid #1e3a5c;
        border-radius: 12px;
        padding: 15px;
    }

    div[data-testid="stMetricLabel"] {
        color: #a8bddc;
    }

    div[data-testid="stMetricValue"] {
        color: #f3f7ff;
    }

    .stButton > button {
        background: linear-gradient(100deg, #087cf5, #653df1);
        color: white;
        border: 0;
        border-radius: 9px;
        min-height: 40px;
    }

    div[data-testid="stFileUploader"] {
        background: #0c192b;
        border: 1px dashed #31577f;
        border-radius: 12px;
        padding: 12px;
    }

    hr {
        border-color: #20344f;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 2. SHARED SESSION STATE
# =========================================================

if "uploaded_df" not in st.session_state:
    st.session_state["uploaded_df"] = None

if "uploaded_dataset_name" not in st.session_state:
    st.session_state["uploaded_dataset_name"] = None

if "latest_analysis_result" not in st.session_state:
    st.session_state["latest_analysis_result"] = None


# =========================================================
# 3. HELPER FUNCTIONS
# =========================================================

def format_number(value):
    """Format numeric values for dashboard cards."""
    if value is None or pd.isna(value):
        return "N/A"

    if abs(float(value)) >= 1_000_000:
        return f"{value:,.2f}"

    return f"{value:,.2f}"


def show_empty_state():
    """Display a message when no dataset has been uploaded."""
    st.info(
        "No dataset uploaded yet. Open **Upload Data** in the sidebar "
        "to begin. No sample data is loaded automatically."
    )


def get_chart_figure(chart):
    """Convert common chart output formats into a Plotly figure."""
    if not isinstance(chart, dict):
        return None

    if isinstance(chart.get("figure"), go.Figure):
        return chart["figure"]

    for key in ("figure_json", "chart_json", "json"):
        value = chart.get(key)

        if isinstance(value, str):
            try:
                return px.from_json(value)
            except Exception:
                try:
                    return go.Figure(json.loads(value))
                except Exception:
                    pass

        if isinstance(value, dict):
            try:
                return go.Figure(value)
            except Exception:
                pass

    if "data" in chart and "layout" in chart:
        try:
            return go.Figure(chart)
        except Exception:
            pass

    return None


def show_analysis_charts(result):
    """Render charts returned by the existing workflow."""
    charts = result.get("charts", [])

    if not charts:
        st.info("No charts were returned for this question.")
        return

    for index, chart in enumerate(charts, start=1):
        title = (
            chart.get("title", f"Chart {index}")
            if isinstance(chart, dict)
            else f"Chart {index}"
        )

        figure = get_chart_figure(chart)

        if figure is not None:
            st.plotly_chart(
                figure,
                use_container_width=True,
                key=f"analysis_chart_{index}",
            )
        else:
            st.caption(
                f"{title}: chart data was returned, but its format "
                "could not be displayed automatically."
            )


def run_analysis(df, question):
    """Run the existing LangGraph workflow on the uploaded dataset."""
    temp_path = None

    try:
        from src.graph.workflow import build_workflow

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".csv",
            encoding="utf-8",
            newline="",
            delete=False,
        ) as temp_file:
            df.to_csv(temp_file, index=False)
            temp_path = temp_file.name

        initial_state = {
            "user_question": question,
            "dataset_path": temp_path,
            "agent_trace": [],
            "tool_results": [],
            "findings": [],
            "charts": [],
            "business_insights": [],
            "errors": [],
            "retry_count": 0,
        }

        result = build_workflow().invoke(initial_state)

        st.session_state["latest_analysis_result"] = result

        # Save history using the project's existing SQLite repository.
        try:
            from database.db import initialize_database
            from database.repositories import save_analysis

            initialize_database()

            save_analysis(
                dataset_name=st.session_state["uploaded_dataset_name"],
                user_question=question,
                verification_status=result.get(
                    "verification_status", "unknown"
                ),
                report_path=result.get("report_path", ""),
                final_answer=result.get("final_answer", ""),
            )
        except Exception as db_error:
            st.warning(
                f"Analysis completed, but history could not be saved: "
                f"{db_error}"
            )

        return result

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


# =========================================================
# 4. SIDEBAR NAVIGATION
# =========================================================

st.sidebar.markdown(
    """
    <div style="padding: 8px 0 14px 0;">
        <div style="font-size: 23px; font-weight: 700;">
            📊 Data Analyst Agent
        </div>
        <div style="color: #9eb4d3; font-size: 12px;">
            MULTI-AGENT ANALYTICS
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.divider()

pages = [
    "Upload Data",
    "Ask & Analyze",
    "Data Explorer",
    "Exploratory Analysis",
    "Data Quality",
    "Workflow Studio",
    "Reports History",
    "Settings",
    "Overview",
]

page = st.sidebar.radio(
    "NAVIGATION",
    pages,
    index=0,
)

df = st.session_state["uploaded_df"]
dataset_name = st.session_state["uploaded_dataset_name"]

if df is not None:
    st.sidebar.success(f"Dataset loaded: {dataset_name}")
    st.sidebar.caption(f"{len(df):,} rows · {len(df.columns)} columns")
else:
    st.sidebar.info("No dataset uploaded")

st.sidebar.divider()
st.sidebar.caption("Python · OpenAI · LangGraph · Plotly · SQLite")


# =========================================================
# 5. HEADER
# =========================================================

st.title("Data Analyst Agent")
st.caption("Multi-Agent Data Analysis & Business Intelligence")
st.divider()


# =========================================================
# 6. UPLOAD DATA
# =========================================================

if page == "Upload Data":
    st.header("Upload your dataset")
    st.write(
        "Start by uploading your own CSV. The same dataset will be "
        "available throughout the dashboard."
    )

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        key="main_csv_uploader",
    )

    if uploaded_file is not None:
        try:
            uploaded_df = pd.read_csv(uploaded_file)

            if uploaded_df.empty:
                st.error("This CSV contains no data rows.")
            else:
                st.session_state["uploaded_df"] = uploaded_df
                st.session_state["uploaded_dataset_name"] = uploaded_file.name

                # Clear results from the previous dataset.
                st.session_state["latest_analysis_result"] = None

                df = uploaded_df
                dataset_name = uploaded_file.name

                st.success(f"Successfully loaded {dataset_name}")

        except Exception as error:
            st.error(f"Unable to read this CSV: {error}")

    df = st.session_state["uploaded_df"]

    if df is None:
        st.markdown("### Get started")
        st.write("Upload a CSV file to unlock the analysis tools.")
        st.caption(
            "Dataset metrics, charts, and insights will not appear "
            "until you upload a file."
        )
    else:
        st.subheader(f"Preview: {st.session_state['uploaded_dataset_name']}")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Rows", f"{len(df):,}")
        col2.metric("Columns", f"{len(df.columns):,}")
        col3.metric("Missing Cells", f"{int(df.isna().sum().sum()):,}")
        col4.metric("Duplicate Rows", f"{int(df.duplicated().sum()):,}")

        st.dataframe(df.head(10), use_container_width=True)


# =========================================================
# 7. ASK & ANALYZE
# =========================================================

elif page == "Ask & Analyze":
    st.header("Ask & Analyze")

    if df is None:
        show_empty_state()
    else:
        st.caption(f"Working with: {dataset_name}")

        question = st.text_area(
            "Ask a question about your data",
            placeholder=(
                "Examples:\n"
                "• Calculate total revenue\n"
                "• Compare revenue by region\n"
                "• Show a chart of profit by category"
            ),
            height=110,
        )

        if st.button("Run Analysis", type="primary"):
            if not question.strip():
                st.warning("Please enter a question.")
            else:
                try:
                    with st.spinner("Your agents are analyzing the dataset..."):
                        result = run_analysis(df, question.strip())

                    st.success("Analysis workflow completed.")

                    st.subheader("Analysis Results")
                    final_answer = result.get("final_answer", "")

                    if final_answer:
                        st.markdown(final_answer)
                    else:
                        st.info("The workflow did not return a final answer.")

                    st.subheader("Business Insights")
                    insights = result.get("business_insights", [])

                    if insights:
                        for insight in insights:
                            st.write(f"• {insight}")
                    else:
                        st.caption("No business insights were returned.")

                    st.subheader("Generated Charts")
                    show_analysis_charts(result)

                    st.subheader("Verification")
                    status = result.get("verification_status", "unknown")
                    if status == "passed":
                        st.success("Critic verification passed.")
                    else:
                        st.warning(f"Verification status: {status}")

                    if result.get("errors"):
                        st.warning("Workflow messages")
                        for error in result["errors"]:
                            st.write(f"• {error}")

                    report_path = result.get("report_path")

                    if report_path and Path(report_path).is_file():
                        with open(report_path, "rb") as report_file:
                            st.download_button(
                                "Download Analysis Report",
                                data=report_file.read(),
                                file_name=Path(report_path).name,
                                mime="text/markdown",
                            )

                except Exception as error:
                    st.error(f"Analysis failed: {error}")
                    st.exception(error)


# =========================================================
# 8. DATA EXPLORER
# =========================================================

elif page == "Data Explorer":
    st.header("Data Explorer")

    if df is None:
        show_empty_state()
    else:
        st.caption(f"Dataset: {dataset_name}")

        search = st.text_input(
            "Filter rows (search across displayed values)",
            placeholder="Enter a value to search",
        )

        display_df = df

        if search.strip():
            mask = df.astype(str).apply(
                lambda column: column.str.contains(
                    search,
                    case=False,
                    regex=False,
                    na=False,
                )
            ).any(axis=1)

            display_df = df[mask]

        st.caption(f"Showing {len(display_df):,} of {len(df):,} rows")
        st.dataframe(display_df, use_container_width=True, height=450)

        st.download_button(
            "Download Current Dataset",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name=dataset_name or "dataset.csv",
            mime="text/csv",
        )

        with st.expander("Column information"):
            column_info = pd.DataFrame({
                "Column": df.columns,
                "Data Type": df.dtypes.astype(str).values,
                "Missing Values": df.isna().sum().values,
                "Unique Values": df.nunique(dropna=True).values,
            })
            st.dataframe(column_info, use_container_width=True)


# =========================================================
# 9. EXPLORATORY DATA ANALYSIS
# =========================================================

elif page == "Exploratory Analysis":
    st.header("Exploratory Data Analysis")

    if df is None:
        show_empty_state()
    else:
        numeric_columns = df.select_dtypes(include="number").columns.tolist()

        categorical_columns = df.select_dtypes(
            include=["object", "category", "bool"]
        ).columns.tolist()

        date_columns = list(
            df.select_dtypes(include=["datetime", "datetimetz"]).columns
        )

        # Detect date columns stored as text.
        for column in df.select_dtypes(include="object").columns:
            if column not in date_columns:
                parsed = pd.to_datetime(df[column], errors="coerce")
                if len(df) and parsed.notna().mean() >= 0.8:
                    date_columns.append(column)

        st.caption(
            f"{len(df):,} rows · {len(df.columns)} columns · "
            f"{len(numeric_columns)} numeric columns"
        )

        # Distribution and box plot.
        st.subheader("1. Numerical Distribution")

        if numeric_columns:
            selected_numeric = st.selectbox(
                "Select a numerical column",
                numeric_columns,
                key="eda_distribution",
            )

            left, right = st.columns(2)

            with left:
                fig = px.histogram(
                    df,
                    x=selected_numeric,
                    marginal="box",
                    title=f"Distribution of {selected_numeric}",
                    template="plotly_dark",
                )
                st.plotly_chart(fig, use_container_width=True)

            with right:
                fig = px.box(
                    df,
                    y=selected_numeric,
                    title=f"Box Plot: {selected_numeric}",
                    template="plotly_dark",
                )
                st.plotly_chart(fig, use_container_width=True)

            valid_values = df[selected_numeric].dropna()

            if not valid_values.empty:
                metrics = st.columns(4)
                metrics[0].metric("Mean", format_number(valid_values.mean()))
                metrics[1].metric("Median", format_number(valid_values.median()))
                metrics[2].metric("Minimum", format_number(valid_values.min()))
                metrics[3].metric("Maximum", format_number(valid_values.max()))
        else:
            st.info("No numerical columns are available.")

        # Categorical counts.
        st.subheader("2. Categorical Analysis")

        if categorical_columns:
            selected_category = st.selectbox(
                "Select a categorical column",
                categorical_columns,
                key="eda_category",
            )

            category_counts = (
                df[selected_category]
                .fillna("Missing")
                .astype(str)
                .value_counts()
                .head(20)
                .rename_axis(selected_category)
                .reset_index(name="Count")
            )

            fig = px.bar(
                category_counts,
                x=selected_category,
                y="Count",
                title=f"Top Categories: {selected_category}",
                template="plotly_dark",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No categorical columns are available.")

        # Scatter plot.
        st.subheader("3. Relationship Analysis")

        if len(numeric_columns) >= 2:
            left, right = st.columns(2)

            with left:
                x_column = st.selectbox(
                    "X-axis",
                    numeric_columns,
                    key="eda_x",
                )

            with right:
                default_y = 1 if len(numeric_columns) > 1 else 0
                y_column = st.selectbox(
                    "Y-axis",
                    numeric_columns,
                    index=default_y,
                    key="eda_y",
                )

            color_options = ["None"] + categorical_columns
            color_column = st.selectbox(
                "Optional category coloring",
                color_options,
                key="eda_color",
            )

            fig = px.scatter(
                df,
                x=x_column,
                y=y_column,
                color=None if color_column == "None" else color_column,
                title=f"{y_column} vs {x_column}",
                template="plotly_dark",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Two numerical columns are needed for a scatter plot.")

        # Correlation heatmap.
        st.subheader("4. Correlation Heatmap")

        if len(numeric_columns) >= 2:
            correlation = df[numeric_columns].corr()

            fig = px.imshow(
                correlation,
                text_auto=".2f",
                aspect="auto",
                color_continuous_scale="RdBu",
                zmin=-1,
                zmax=1,
                title="Numerical Feature Correlations",
                template="plotly_dark",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Two numerical columns are needed for correlation.")

        # Time-series trend.
        st.subheader("5. Trend Analysis")

        if date_columns and numeric_columns:
            left, right = st.columns(2)

            with left:
                date_column = st.selectbox(
                    "Date column",
                    date_columns,
                    key="eda_date",
                )

            with right:
                value_column = st.selectbox(
                    "Metric",
                    numeric_columns,
                    key="eda_trend_metric",
                )

            trend_df = df[[date_column, value_column]].copy()
            trend_df[date_column] = pd.to_datetime(
                trend_df[date_column],
                errors="coerce",
            )
            trend_df = trend_df.dropna(subset=[date_column, value_column])

            trend_df = (
                trend_df.groupby(date_column, as_index=False)[value_column]
                .mean()
                .sort_values(date_column)
            )

            if not trend_df.empty:
                fig = px.line(
                    trend_df,
                    x=date_column,
                    y=value_column,
                    markers=True,
                    title=f"{value_column} Over Time",
                    template="plotly_dark",
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No valid date and metric values were found.")
        else:
            st.info(
                "Trend analysis needs a recognizable date column and "
                "at least one numerical column."
            )


# =========================================================
# 10. DATA QUALITY
# =========================================================

elif page == "Data Quality":
    st.header("Data Quality")

    if df is None:
        show_empty_state()
    else:
        col1, col2, col3 = st.columns(3)

        col1.metric("Missing Cells", f"{int(df.isna().sum().sum()):,}")
        col2.metric("Duplicate Rows", f"{int(df.duplicated().sum()):,}")
        col3.metric("Columns", f"{len(df.columns):,}")

        quality_df = pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str).values,
            "Missing Values": df.isna().sum().values,
            "Missing (%)": (df.isna().mean().values * 100).round(2),
            "Unique Values": df.nunique(dropna=True).values,
        })

        st.subheader("Column-level quality")
        st.dataframe(quality_df, use_container_width=True)

        missing_df = quality_df[
            quality_df["Missing Values"] > 0
        ].sort_values("Missing Values", ascending=False)

        if not missing_df.empty:
            st.subheader("Missing values by column")

            fig = px.bar(
                missing_df,
                x="Column",
                y="Missing Values",
                title="Missing Values",
                template="plotly_dark",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("No missing values found.")


# =========================================================
# 11. WORKFLOW STUDIO
# =========================================================

elif page == "Workflow Studio":
    st.header("Workflow Studio")
    result = st.session_state["latest_analysis_result"]

    if not result:
        st.info("Run an analysis to inspect agent execution.")
    else:
        status = result.get("verification_status", "unknown")
        st.metric("Verification Status", status.title())

        trace = result.get("agent_trace", [])

        if trace:
            st.subheader("Agent Execution Trace")

            for item in trace:
                agent_name = item.get("agent", "Unknown agent")

                with st.expander(agent_name.replace("_", " ").title()):
                    st.json(item)
        else:
            st.info("No agent trace was returned.")

        if result.get("errors"):
            st.subheader("Workflow Messages")
            for error in result["errors"]:
                st.write(f"• {error}")


# =========================================================
# 12. REPORTS HISTORY
# =========================================================

elif page == "Reports History":
    st.header("Reports History")

    try:
        from database.db import initialize_database
        from database.repositories import get_analysis_history

        initialize_database()
        history = get_analysis_history(limit=100)

        if history:
            history_df = pd.DataFrame(history)
            st.dataframe(history_df, use_container_width=True)

            ids = [item["id"] for item in history]

            selected_id = st.selectbox(
                "Select an analysis",
                ids,
                format_func=lambda value: f"Analysis #{value}",
            )

            selected = next(
                item for item in history if item["id"] == selected_id
            )

            st.subheader("Saved Answer")
            st.write(selected.get("final_answer") or "No answer saved.")

            report_path = selected.get("report_path")

            if report_path and Path(report_path).is_file():
                with open(report_path, "rb") as report_file:
                    st.download_button(
                        "Download Report",
                        data=report_file.read(),
                        file_name=Path(report_path).name,
                        mime="text/markdown",
                    )
        else:
            st.info("No saved analyses yet. Run an analysis first.")

    except Exception as error:
        st.error(f"Could not load analysis history: {error}")


# =========================================================
# 13. SETTINGS
# =========================================================

elif page == "Settings":
    st.header("Settings")

    st.write("**Application:** Data Analyst Agent")
    st.write("**LLM routing:** OpenAI Supervisor")
    st.write("**Workflow:** LangGraph")
    st.write("**Data processing:** Pandas")
    st.write("**Visualization:** Plotly")
    st.write("**History:** SQLite")

    st.subheader("API Configuration")

    # Show whether a key is configured, never display the key itself.
    from dotenv import load_dotenv

    load_dotenv()
    if os.getenv("OPENAI_API_KEY"):
        st.success("OpenAI API key detected in the environment.")
    else:
        st.warning("OPENAI_API_KEY was not found in the environment.")

    st.caption(
        "Keep your API key in .env and do not commit that file to GitHub."
    )


# =========================================================
# 14. OVERVIEW — LAST IN SIDEBAR
# =========================================================

elif page == "Overview":
    st.header("Overview")
    st.caption("Summary of your uploaded dataset and latest analysis.")

    if df is None:
        show_empty_state()
    else:
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Rows", f"{len(df):,}")
        col2.metric("Columns", f"{len(df.columns):,}")
        col3.metric("Missing Cells", f"{int(df.isna().sum().sum()):,}")
        col4.metric("Duplicate Rows", f"{int(df.duplicated().sum()):,}")

        st.subheader("Dataset Preview")
        st.dataframe(df.head(10), use_container_width=True)

        result = st.session_state["latest_analysis_result"]

        if result:
            st.subheader("Latest Business Insights")

            for insight in result.get("business_insights", []):
                st.write(f"• {insight}")

            st.caption(
                "Verification status: "
                f"{result.get('verification_status', 'unknown')}"
            )

            st.subheader("Latest Analysis Charts")
            show_analysis_charts(result)

        else:
            st.info(
                "Dataset loaded. Open Ask & Analyze to generate "
                "business insights and charts."
            )


# =========================================================
# 15. FOOTER
# =========================================================

st.divider()
st.caption(
    "Data Analyst Agent · OpenAI · LangGraph · Pandas · Plotly · SQLite"
)
