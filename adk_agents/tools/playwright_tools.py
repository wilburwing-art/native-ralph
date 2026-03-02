"""Tools that bridge to existing Node.js Playwright infrastructure."""

import subprocess
from pathlib import Path

from google.adk.tools.tool_context import ToolContext

from adk_agents.config import get_browser_tests_dir, get_target_url


def take_screenshot(
    url: str | None = None,
    output_path: str | None = None,
    tool_context: ToolContext | None = None,
) -> dict:
    """Capture a screenshot of a web page using the existing screenshot.js script.

    Args:
        url: URL to screenshot. Defaults to ADK_TARGET_URL env var.
        output_path: Where to save the PNG. Defaults to browser-tests/snapshots/current.png.

    Returns:
        dict with status, path to saved screenshot, and any error message.
    """
    browser_tests = get_browser_tests_dir()
    screenshot_script = browser_tests / "scripts" / "screenshot.js"

    if not screenshot_script.exists():
        return {"status": "error", "error": f"screenshot.js not found at {screenshot_script}"}

    url = url or get_target_url()
    if output_path is None:
        snapshots_dir = browser_tests / "snapshots"
        snapshots_dir.mkdir(exist_ok=True)
        output_path = str(snapshots_dir / "current.png")

    result = subprocess.run(
        ["node", str(screenshot_script), url, output_path],
        capture_output=True,
        text=True,
        cwd=str(browser_tests),
        timeout=60,
    )

    if result.returncode != 0:
        return {"status": "error", "error": result.stderr.strip() or result.stdout.strip()}

    if tool_context is not None:
        tool_context.state["last_screenshot"] = output_path

    return {"status": "ok", "path": output_path, "output": result.stdout.strip()}


def run_tests(
    test_file: str | None = None,
    tool_context: ToolContext | None = None,
) -> dict:
    """Run Playwright browser tests using the existing test infrastructure.

    Args:
        test_file: Specific test file to run (relative to browser-tests/tests/).
                   Runs all tests if omitted.

    Returns:
        dict with status (pass/fail), stdout, stderr, and return code.
    """
    browser_tests = get_browser_tests_dir()

    cmd = ["npx", "playwright", "test"]
    if test_file:
        cmd.append(f"tests/{test_file}")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(browser_tests),
        timeout=120,
    )

    passed = result.returncode == 0
    output = {
        "status": "pass" if passed else "fail",
        "return_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }

    if tool_context is not None:
        tool_context.state["last_test_result"] = output["status"]
        tool_context.state["last_test_output"] = result.stdout[-2000:] if result.stdout else ""

    return output


def compare_screenshots(
    baseline_path: str,
    current_path: str,
    threshold: float = 0.1,
    tool_context: ToolContext | None = None,
) -> dict:
    """Compare two screenshots using the existing validate.js script.

    Args:
        baseline_path: Path to baseline PNG.
        current_path: Path to current PNG.
        threshold: Maximum allowed difference percentage (default 0.1%).

    Returns:
        dict with match status, diff percentage, and output text.
    """
    browser_tests = get_browser_tests_dir()
    validate_script = browser_tests / "scripts" / "validate.js"

    if not validate_script.exists():
        return {"status": "error", "error": f"validate.js not found at {validate_script}"}

    result = subprocess.run(
        ["node", str(validate_script), baseline_path, current_path, str(threshold)],
        capture_output=True,
        text=True,
        cwd=str(browser_tests),
        timeout=60,
    )

    matched = result.returncode == 0
    output = {
        "status": "match" if matched else "mismatch",
        "matched": matched,
        "output": result.stdout.strip(),
    }

    if tool_context is not None:
        tool_context.state["last_comparison"] = output["status"]

    return output
