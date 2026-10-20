import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "Data Analyst Agent"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
DATABASE_PATH = os.getenv(
    "DATABASE_PATH", "data_analyst_agent.db"
)
MAX_AGENT_RETRIES = int(
    os.getenv("MAX_AGENT_RETRIES", "2")
)
