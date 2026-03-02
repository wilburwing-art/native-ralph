"""Tests for agent wiring and pipeline structure."""

from google.adk.agents import SequentialAgent, LoopAgent, LlmAgent

from adk_agents.agent import root_agent, refinement_loop
from adk_agents.agents import (
    screenshot_agent,
    analyzer_agent,
    fixer_agent,
    validator_agent,
    reporter_agent,
)


class TestAgentDefinitions:
    def test_screenshot_agent_is_llm_agent(self):
        assert isinstance(screenshot_agent, LlmAgent)
        assert screenshot_agent.name == "ScreenshotAgent"

    def test_analyzer_agent_is_llm_agent(self):
        assert isinstance(analyzer_agent, LlmAgent)
        assert analyzer_agent.name == "AnalyzerAgent"

    def test_fixer_agent_is_llm_agent(self):
        assert isinstance(fixer_agent, LlmAgent)
        assert fixer_agent.name == "FixerAgent"

    def test_validator_agent_is_llm_agent(self):
        assert isinstance(validator_agent, LlmAgent)
        assert validator_agent.name == "ValidatorAgent"

    def test_reporter_agent_is_llm_agent(self):
        assert isinstance(reporter_agent, LlmAgent)
        assert reporter_agent.name == "ReporterAgent"

    def test_screenshot_agent_has_tools(self):
        assert len(screenshot_agent.tools) == 2

    def test_analyzer_agent_has_tools(self):
        assert len(analyzer_agent.tools) == 2

    def test_fixer_agent_has_tools(self):
        assert len(fixer_agent.tools) == 3

    def test_validator_agent_has_tools(self):
        assert len(validator_agent.tools) == 4

    def test_reporter_agent_has_no_tools(self):
        assert len(reporter_agent.tools) == 0

    def test_agents_have_output_keys(self):
        assert screenshot_agent.output_key == "screenshot_summary"
        assert analyzer_agent.output_key == "analysis"
        assert fixer_agent.output_key == "fixes_applied"
        assert validator_agent.output_key == "validation_result"
        assert reporter_agent.output_key == "final_report"


class TestPipelineStructure:
    def test_root_agent_is_sequential(self):
        assert isinstance(root_agent, SequentialAgent)
        assert root_agent.name == "ui_refinement_pipeline"

    def test_root_has_three_sub_agents(self):
        assert len(root_agent.sub_agents) == 3

    def test_root_sub_agent_order(self):
        agents = root_agent.sub_agents
        assert agents[0].name == "ScreenshotAgent"
        assert agents[1].name == "refinement_loop"
        assert agents[2].name == "ReporterAgent"

    def test_refinement_loop_is_loop_agent(self):
        assert isinstance(refinement_loop, LoopAgent)
        assert refinement_loop.name == "refinement_loop"

    def test_refinement_loop_has_max_iterations(self):
        assert refinement_loop.max_iterations > 0

    def test_refinement_loop_sub_agents(self):
        agents = refinement_loop.sub_agents
        assert len(agents) == 3
        assert agents[0].name == "AnalyzerAgent"
        assert agents[1].name == "FixerAgent"
        assert agents[2].name == "ValidatorAgent"


class TestConfig:
    def test_default_model(self):
        from adk_agents.config import get_model
        # Default or env-overridden, should be a non-empty string
        model = get_model()
        assert isinstance(model, str)
        assert len(model) > 0

    def test_default_max_iterations(self):
        from adk_agents.config import get_max_iterations
        iters = get_max_iterations()
        assert isinstance(iters, int)
        assert iters > 0

    def test_default_target_url(self):
        from adk_agents.config import get_target_url
        url = get_target_url()
        assert url.startswith("http")
