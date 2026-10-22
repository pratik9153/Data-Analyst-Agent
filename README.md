# Data Analyst Agent

Data Analyst Agent is an AI-powered application designed to help users explore datasets, understand key metrics, create visualizations, and ask questions about their data using natural language.

## Features

- Upload datasets for analysis.
- Review dataset dimensions, column types, missing values, and descriptive statistics.
- Calculate and display key performance indicators (KPIs).
- Explore data through interactive visualizations.
- Ask questions about the dataset through an AI Analyst interface.
- View AI-generated explanations and insights based on the available data.
- 

<img width="1872" height="797" alt="Screenshot 2026-10-20 210819" src="https://github.com/user-attachments/assets/63a5e0d1-db8f-4ccb-a7c4-0a68b7c82496" />
<img width="1912" height="872" alt="Screenshot 2026-10-20 210848" src="https://github.com/user-attachments/assets/b52cb1ff-34f8-4fb8-932c-396ef7c09023" />
<img width="1902" height="812" alt="Screenshot 2026-10-20 210729" src="https://github.com/user-attachments/assets/d84304e3-73d2-4c99-8675-4d9382333d8a" />
<img width="1902" height="897" alt="Screenshot 2026-10-20 210639" src="https://github.com/user-attachments/assets/fdb1ce88-e47b-43a4-be88-1bcca53073c0" />



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
git clone https://github.com/pratik9153/Data-Analyst-Agent.git
cd Data-Analyst-Agent
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

