"""FixerAgent — applies code changes to fix identified UI issues."""

from google.adk.agents import LlmAgent

from adk_agents.config import get_model
from adk_agents.tools.file_tools import read_file, write_file, list_files

fixer_agent = LlmAgent(
    name="FixerAgent",
    model=get_model(),
    description="Applies code changes to fix UI issues identified by the analyzer.",
    instruction="""You are a code fixer inside a UI refinement loop.

Analysis of issues to fix:
{analysis}

Your job:
1. Read each file that needs changes using read_file.
2. Apply the fixes described in the analysis using write_file.
3. Only change what is necessary — minimal, targeted fixes.
4. Summarize each change you made (file path + what changed).

Do not introduce new features or refactor unrelated code.
""",
    tools=[read_file, write_file, list_files],
    output_key="fixes_applied",
)
