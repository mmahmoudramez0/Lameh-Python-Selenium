import os
from dotenv import load_dotenv

# Load environment variables from .env file (if exists)
# CI/CD pipeline variables will override .env values
load_dotenv()


def get_base_url():
    """
    Returns the base URL based on the ENV environment variable.
    
    Usage:
        - Local: Create .env file with ENV=test (or uat/main)
        - Terminal: $env:ENV="test"; pytest
        - CI/CD: Set ENV in pipeline configuration
    
    Returns:
        str: Base URL for the specified environment
    
    Raises:
        Exception: If ENV is set to an unknown environment
    """
    env = os.environ.get("ENV", "test")

    if env.lower() == "test":
        return "https://frontend-dev-36462279645.me-central2.run.app"
    elif env.lower() == "main":
        return "https://core.lameh.ai/"
    elif env.lower() == "uat":
        return "https://frontend-dev-36462279645.me-central2.app"
    else:
        raise Exception(f"Unknown environment: {env}")
