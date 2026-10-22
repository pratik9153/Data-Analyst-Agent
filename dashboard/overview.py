
"""Overview dashboard page."""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


SAMPLE_DATA = Path("data/sample/sales.csv.csv")


def load_dashboard_data(df=None):
    """Use uploaded data, or load the sample dataset if available."""
    if df is not None:
        return df

    if SAMPLE_DATA.exists():
        try:
            return pd.read_csv(SAMPLE_DATA)
        except (OSError, ValueError, UnicodeDecodeError):
            return None

    return None


def metric_card(label, value, help_text=None):
    st.metric(label=label, value=value, help=help_text)


def render_overview(df=None):
    """Render the main analytics dashboard."""

    df = load_dashboard_data(df)

    header_left, header_right = st.columns([4, 1])

    with header_left:
        st.title("Welcome to Data Analyst Agent 👋")
        st.caption(
            "Upload your dataset and let your analysis agents uncover "
            "useful patterns and business insights."
        )

    with header_right:
        st.markdown("**MULTI-AGENT ANALYTICS**")
        st.caption("Python · LangGraph · Plotly")

    st.divider()

    if df is None:
        st.info("Upload a CSV file in Data Explorer to get started.")
        st.markdown("### Your analytics workspace")
        st.markdown(
            "- Explore dataset structure and data quality.\n"
            "- Calculate metrics and compare categories.\n"
            "- Generate interactive charts.\n"
            "- Run multi-agent analysis and export reports."
        )
        return

    # Dataset information
    numeric_columns = df.select_dtypes(include="number").columns.tolist()
    categorical_columns = [
        col for col in df.columns
        if col not in numeric_columns
    ]

    missing_count = int(df.isna().sum().sum())
    duplicate_count = int(df.duplicated().sum())
    missing_pct = (
        missing_count / (len(df) * len(df.columns)) * 100
        if len(df) and len(df.columns)
        else 0
    )

    st.subheader("Dataset overview")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        metric_card("Rows", f"{len(df):,}")

    with col2:
        metric_card("Columns", f"{len(df.columns):,}")

    with col3:
        metric_card("Numerical", len(numeric_columns))

    with col4:
        metric_card("Missing values", f"{missing_pct:.2f}%")

    with col5:
        metric_card("Duplicate rows", f"{duplicate_count:,}")

    # Overview tabs
    tab_overview, tab_quality, tab_columns = st.tabs(
        ["Overview", "Data Quality", "Column Details"]
    )

    with tab_overview:
        st.subheader("Dataset preview")
        st.dataframe(df.head(10), use_container_width=True)

        st.subheader("Explore your business data")

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            if "region" in df.columns and "revenue" in df.columns:
                region_data = df.groupby(
                    "region", dropna=False
                )["revenue"].sum().reset_index()
                region_data["region"] = (
                    region_data["region"].fillna("Unknown").astype(str)
                )

                fig = px.bar(
                    region_data,
                    x="region",
                    y="revenue",
                    title="Revenue by Region",
                    color="region",
                    template="plotly_dark",
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    showlegend=False,
                    margin=dict(l=10, r=10, t=55, b=10),
                )
                st.plotly_chart(fig, use_container_width=True)

            elif numeric_columns:
                selected = st.selectbox(
                    "Choose a numerical column",
                    numeric_columns,
                    key="overview_hist_column",
                )
                fig = px.histogram(
                    df,
                    x=selected,
                    title=f"Distribution of {selected}",
                    template="plotly_dark",
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                )
                st.plotly_chart(fig, use_container_width=True)

            else:
                st.info("No numerical columns available for charting.")

        with chart_col2:
            if "category" in df.columns and "profit" in df.columns:
                category_data = df.groupby(
                    "category", dropna=False
                )["profit"].sum().reset_index()
                category_data["category"] = (
                    category_data["category"].fillna("Unknown").astype(str)
                )

                fig = px.bar(
                    category_data,
                    x="category",
                    y="profit",
                    title="Profit by Category",
                    color="category",
                    template="plotly_dark",
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    showlegend=False,
                    margin=dict(l=10, r=10, t=55, b=10),
                )
                st.plotly_chart(fig, use_container_width=True)

            elif len(numeric_columns) >= 2:
                x_col = st.selectbox(
                    "X-axis",
                    numeric_columns,
                    index=0,
                    key="overview_x_column",
                )
                y_options = [c for c in numeric_columns if c != x_col]
                y_col = st.selectbox(
                    "Y-axis",
                    y_options,
                    key="overview_y_column",
                )
                fig = px.scatter(
                    df,
                    x=x_col,
                    y=y_col,
                    title=f"{y_col} vs {x_col}",
                    template="plotly_dark",
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                )
                st.plotly_chart(fig, use_container_width=True)

            else:
                st.info("More numerical columns are needed for comparisons.")

    with tab_quality:
        st.subheader("Data quality")

        quality = pd.DataFrame({
            "Column": df.columns,
            "Data type": df.dtypes.astype(str).values,
            "Missing values": df.isna().sum().values,
            "Missing (%)": (
                df.isna().mean().values * 100
            ).round(2),
            "Unique values": df.nunique(dropna=True).values,
        })

        st.dataframe(quality, use_container_width=True)

        if missing_count:
            st.warning(
                f"The dataset contains {missing_count:,} missing cells."
            )
        else:
            st.success("No missing values detected.")

        if duplicate_count:
            st.warning(
                f"The dataset contains {duplicate_count:,} duplicate rows."
            )
        else:
            st.success("No duplicate rows detected.")

    with tab_columns:
        st.subheader("Column details")

        selected_column = st.selectbox(
            "Select a column",
            df.columns.tolist(),
            key="overview_column_details",
        )

        series = df[selected_column]

        st.write("**Data type:**", str(series.dtype))
        st.write("**Missing values:**", int(series.isna().sum()))
        st.write("**Unique values:**", int(series.nunique(dropna=True)))

        if pd.api.types.is_numeric_dtype(series):
            st.dataframe(
                series.describe().to_frame("Statistics"),
                use_container_width=True,
            )
        else:
            st.dataframe(
                series.value_counts(dropna=False)
                .head(15)
                .rename_axis(selected_column)
                .reset_index(name="Count"),
                use_container_width=True,
            )
