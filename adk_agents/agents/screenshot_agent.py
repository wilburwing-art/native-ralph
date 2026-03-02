"""ScreenshotAgent — captures baseline screenshot and runs initial tests."""

from google.adk.agents import LlmAgent

from adk_agents.config import get_model
from adk_agents.tools.playwright_tools import take_screenshot, run_tests

screenshot_agent = LlmAgent(
    name="ScreenshotAgent",
    model=get_model(),
    description="Captures a baseline screenshot and runs the initial browser test suite.",
    instruction="""You are the first step in a UI refinement pipeline.

Your job:
1. Call take_screenshot to capture the current state of the page at the target URL.
2. Call run_tests to execute the full Playwright test suite.
3. Summarize what you observe: which tests passed, which failed, and any errors.

Store your findings so downstream agents can use them.
The target URL is: {target_url}
""",
    tools=[take_screenshot, run_tests],
    output_key="screenshot_summary",
)
