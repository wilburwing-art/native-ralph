"""Loop control tool for ADK LoopAgent termination."""

from google.adk.tools.tool_context import ToolContext


def exit_loop(reason: str, tool_context: ToolContext) -> dict:
    """Signal that the refinement loop should terminate.

    Call this when all tests pass or the task is complete.
    This sets escalate=True on the ToolContext, causing the
    enclosing LoopAgent to stop iterating.

    Args:
        reason: Explanation of why the loop is exiting (e.g. "all tests pass").

    Returns:
        dict confirming the loop exit was triggered.
    """
    tool_context.actions.escalate = True
    return {"status": "loop_exited", "reason": reason}
