"""ValidatorAgent — re-runs tests and exits the loop when all pass."""

from google.adk.agents import LlmAgent

from adk_agents.config import get_model
from adk_agents.tools.playwright_tools import run_tests, take_screenshot, compare_screenshots
from adk_agents.tools.loop_control import exit_loop

validator_agent = LlmAgent(
    name="ValidatorAgent",
    model=get_model(),
    description="Re-runs tests after fixes and exits the loop when all tests pass.",
    instruction="""You are a validation agent inside a UI refinement loop.

Fixes that were applied:
{fixes_applied}

Your job:
1. Call run_tests to re-run the full Playwright test suite.
2. If ALL tests pass: call exit_loop with a success reason. The loop will stop.
3. If tests still fail: do NOT call exit_loop. Summarize what still fails
   so the next iteration of AnalyzerAgent can pick up where you left off.

Only call exit_loop when you are confident all tests pass.
""",
    tools=[run_tests, take_screenshot, compare_screenshots, exit_loop],
    output_key="validation_result",
)
