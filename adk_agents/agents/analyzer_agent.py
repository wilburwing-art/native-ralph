"""AnalyzerAgent — reads test failures and identifies UI issues to fix."""

from google.adk.agents import LlmAgent

from adk_agents.config import get_model
from adk_agents.tools.file_tools import read_file, list_files

analyzer_agent = LlmAgent(
    name="AnalyzerAgent",
    model=get_model(),
    description="Analyzes test failures and identifies the root cause of UI issues.",
    instruction="""You are a UI issue analyzer inside a refinement loop.

Previous test results:
{last_test_output}

Your job:
1. Read the test output above and identify which tests failed and why.
2. Use read_file and list_files to examine the relevant source files.
3. Determine what specific code changes would fix each failing test.
4. Write a clear, actionable analysis listing each issue and its proposed fix.

Be specific about file paths and line-level changes needed.
""",
    tools=[read_file, list_files],
    output_key="analysis",
)
