"""Programmatic runner with CLI for the ADK UI refinement pipeline."""

import argparse
import asyncio
import sys

from google.adk.runners import InMemoryRunner
from google.genai import types as genai_types

from adk_agents.agent import root_agent


async def run_pipeline(target_url: str, max_iterations: int | None = None) -> str:
    """Run the UI refinement pipeline programmatically.

    Args:
        target_url: URL of the site to test.
        max_iterations: Override for max loop iterations.

    Returns:
        The final report text from the pipeline.
    """
    import os

    os.environ["ADK_TARGET_URL"] = target_url
    if max_iterations is not None:
        os.environ["ADK_MAX_ITERATIONS"] = str(max_iterations)

    runner = InMemoryRunner(agent=root_agent, app_name="ralph_loop_adk")
    user_id = "cli_user"
    session_id = "pipeline_run"

    message = genai_types.Content(
        role="user",
        parts=[genai_types.Part(text=f"Run the UI refinement pipeline on {target_url}")],
    )

    final_text = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=message,
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    final_text = part.text
                    print(f"[{event.author}] {part.text[:200]}")

    return final_text


def main():
    parser = argparse.ArgumentParser(
        prog="adk-pipeline",
        description="Run the Ralph Loop ADK UI refinement pipeline.",
    )
    parser.add_argument(
        "--url",
        default="http://localhost:3000",
        help="Target URL to test (default: http://localhost:3000)",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=None,
        help="Maximum refinement loop iterations (default: from ADK_MAX_ITERATIONS or 5)",
    )
    args = parser.parse_args()

    print(f"Starting ADK UI refinement pipeline for {args.url}")
    result = asyncio.run(run_pipeline(args.url, args.max_iterations))
    print("\n--- Final Report ---")
    print(result)


if __name__ == "__main__":
    main()
