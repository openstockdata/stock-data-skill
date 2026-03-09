"""Load .env file for API keys before any tool function is called."""
import os
from pathlib import Path


def load_env():
    """Load .env from multiple search paths (first found wins).

    Search order:
    1. $CWD/.env
    2. ~/.stock-data.env
    3. Package root .env

    Uses override=False so existing environment variables take precedence.
    """
    from dotenv import load_dotenv

    search_paths = [
        Path.cwd() / ".env",
        Path.home() / ".stock-data.env",
        Path(__file__).parent.parent / ".env",
    ]
    for p in search_paths:
        if p.exists():
            load_dotenv(p, override=False)
            return
