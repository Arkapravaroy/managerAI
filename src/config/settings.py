import os
import getpass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def _set_env(var: str):
    """Set environment variable with user input if not already set."""
    # Check if the variable is set in the OS environment
    env_value = os.environ.get(var)
    if not env_value:
        # If not set, prompt the user for input
        env_value = getpass.getpass(f"{var}: ")

    # Set the environment variable for the current process
    os.environ[var] = env_value

def setup_environment():
    """Setup all required environment variables."""
    # Setup LangSmith (optional)
    _set_env("LANGSMITH_API_KEY")
    os.environ["LANGSMITH_TRACING"] = "true"
    os.environ["LANGSMITH_PROJECT"] = "manager-ai"

    # Setup required API keys
    _set_env("GROQ_API_KEY")
    _set_env("TAVILY_API_KEY")

# Model configuration
MODEL_NAME = "qwen-qwq-32b"
MODEL_TEMPERATURE = 0
