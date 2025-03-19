import os
from pathlib import Path
from dotenv import load_dotenv

def is_github_actions():
    """Verify if the script is running on GitHub Actions."""
    return os.getenv("GITHUB_ACTIONS") is not None


def get_workspace():
    """Verify if the script is running on GitHub Actions and return the workspace directory."""
    return Path(os.getenv("GITHUB_WORKSPACE", ".")) if is_github_actions() else Path(".")

def load_env_if_local():
    """Load .env file if running locally."""
    if not is_github_actions():
        load_dotenv()





