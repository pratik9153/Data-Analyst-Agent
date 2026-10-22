# Data Analyst Agent

Data Analyst Agent is an AI-powered application designed to help users explore datasets, understand key metrics, create visualizations, and ask questions about their data using natural language.

## Features

- Upload datasets for analysis.
- Review dataset dimensions, column types, missing values, and descriptive statistics.
- Calculate and display key performance indicators (KPIs).
- Explore data through interactive visualizations.
- Ask questions about the dataset through an AI Analyst interface.
- View AI-generated explanations and insights based on the available data.

## Technology Stack

- **Python** for application logic and data analysis.
- **Streamlit** for the interactive web interface.
- **Pandas** for data processing and analysis.
- **Plotly** for interactive visualizations.
- **Large Language Models (LLMs)** for natural-language analysis and insight generation.

## How It Works

1. Upload a dataset.
2. Inspect the dataset and its data-quality information.
3. Review key metrics and descriptive statistics.
4. Explore charts and visualizations.
5. Ask questions through the AI Analyst interface.
6. Review the generated explanations and insights.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/pratik9153/AI-Data-Analyst-Agent.git
cd AI-Data-Analyst-Agent
```

### 2. Create and activate a virtual environment

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux**

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

If your implementation requires an LLM API key, add it to a local `.env` file using the environment variable name expected by your code. Do not upload API keys or secrets to GitHub.

### 5. Run the application

If the application entry point is `app.py`, run:

```bash
streamlit run app.py
```

## Use Cases

- Analyze sales, customer, or operational datasets.
- Identify missing values and review data quality.
- Summarize key metrics.
- Visualize trends and compare categories.
- Ask questions about data in natural language.

## Future Improvements

- Multi-agent analysis workflow.
- Improved dataset validation and error handling.
- Context-aware chart recommendations.
- AI responses grounded in computed results.
- Exportable analysis reports.
- Automated testing.

## Responsible Use

AI-generated insights should be checked against the underlying data. Do not upload confidential or personally identifiable information unless you are authorized to do so. Keep API keys and other secrets out of source control.

## Author

**Pratik Choudhary**

GitHub: [pratik9153](https://github.com/pratik9153)

