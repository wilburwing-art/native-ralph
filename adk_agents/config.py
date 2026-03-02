"""Environment-based configuration for ADK pipeline."""

import os
from pathlib import Path


def get_project_root() -> Path:
    """Return the ralph-loop project root directory."""
    return Path(__file__).parent.parent


def get_browser_tests_dir() -> Path:
    """Return path to browser-tests directory."""
    env_val = os.environ.get("ADK_BROWSER_TESTS_DIR")
    if env_val:
        return Path(env_val)
    return get_project_root() / "browser-tests"


def get_target_url() -> str:
    return os.environ.get("ADK_TARGET_URL", "http://localhost:3000")


def get_max_iterations() -> int:
    return int(os.environ.get("ADK_MAX_ITERATIONS", "5"))


def get_model() -> str:
    return os.environ.get("ADK_MODEL", "gemini-2.0-flash")
