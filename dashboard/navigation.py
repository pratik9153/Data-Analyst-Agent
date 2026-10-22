
"""Dashboard navigation."""

import streamlit as st


PAGES = [
    "Overview",
    "Ask & Analyze",
    "Data Explorer",
    "Data Quality",
    "Exploratory Analysis",
    "Reports History",
    "Workflow Studio",
    "Settings",
]


def render_navigation() -> str:
    """Display sidebar navigation and return the selected page."""

    st.sidebar.title("Data Analyst Agent")
    st.sidebar.caption("Multi-Agent Analytics")

    selected_page = st.sidebar.radio(
        "Navigation",
        options=PAGES,
        index=0,
    )

    st.sidebar.divider()
    st.sidebar.caption("Python • LangGraph • Pandas • Plotly")

    return selected_page
