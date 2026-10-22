
"""Dataset upload and exploration."""

import streamlit as st
import pandas as pd


def render_data_explorer() -> None:
    """Upload a CSV file and explore its contents."""

    st.title("Data Explorer")
    st.caption("Upload a CSV file to inspect its contents.")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        key="dataset_upload",
    )

    if uploaded_file is None:
        st.info("Choose a CSV file to begin.")
        return

    try:
        df = pd.read_csv(uploaded_file)

        if df.empty:
            st.warning("The uploaded CSV contains no data rows.")
            return

        st.session_state["uploaded_df"] = df
        st.session_state["uploaded_dataset_name"] = uploaded_file.name

        st.success(f"Loaded {uploaded_file.name} successfully.")

        col1, col2, col3 = st.columns(3)
        col1.metric("Rows", f"{len(df):,}")
        col2.metric("Columns", f"{len(df.columns):,}")
        col3.metric(
            "Missing values",
            f"{int(df.isna().sum().sum()):,}",
        )

        st.subheader("Preview")
        st.dataframe(df.head(20), use_container_width=True)

        st.subheader("Column information")
        column_info = pd.DataFrame({
            "Column": df.columns,
            "Data type": df.dtypes.astype(str).values,
            "Missing values": df.isna().sum().values,
            "Unique values": df.nunique(dropna=True).values,
        })
        st.dataframe(column_info, use_container_width=True)

    except (ValueError, UnicodeDecodeError, pd.errors.ParserError) as error:
        st.error(f"Could not read this CSV file: {error}")
