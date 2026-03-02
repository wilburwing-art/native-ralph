"""ReporterAgent — writes a final summary report of the pipeline run."""

from google.adk.agents import LlmAgent

from adk_agents.config import get_model

reporter_agent = LlmAgent(
    name="ReporterAgent",
    model=get_model(),
    description="Writes a final summary report after the refinement pipeline completes.",
    instruction="""You are the final reporter in a UI refinement pipeline.

Initial assessment:
{screenshot_summary}

Final validation:
{validation_result}

Your job:
1. Summarize what the pipeline accomplished.
2. List all issues that were found and fixed.
3. Note the final test status (all passing, or remaining failures).
4. If there are remaining issues, describe what would need to happen next.

Write a clear, concise report suitable for a developer reviewing the changes.
""",
    tools=[],
    output_key="final_report",
)
