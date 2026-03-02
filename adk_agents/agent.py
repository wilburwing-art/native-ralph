"""Pipeline assembly — wires SequentialAgent + LoopAgent for UI refinement."""

from google.adk.agents import SequentialAgent, LoopAgent

from adk_agents.config import get_max_iterations
from adk_agents.agents import (
    screenshot_agent,
    analyzer_agent,
    fixer_agent,
    validator_agent,
    reporter_agent,
)

refinement_loop = LoopAgent(
    name="refinement_loop",
    sub_agents=[analyzer_agent, fixer_agent, validator_agent],
    max_iterations=get_max_iterations(),
)

root_agent = SequentialAgent(
    name="ui_refinement_pipeline",
    description="Multi-agent pipeline that iteratively fixes UI issues using Playwright tests.",
    sub_agents=[screenshot_agent, refinement_loop, reporter_agent],
)
