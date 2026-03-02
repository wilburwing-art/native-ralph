"""Unit tests for ADK pipeline tool functions."""

import os
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from adk_agents.tools.file_tools import read_file, write_file, list_files
from adk_agents.tools.playwright_tools import take_screenshot, compare_screenshots
from adk_agents.tools.loop_control import exit_loop


class TestFileTools:
    def test_read_file_existing(self, tmp_project):
        path = tmp_project / "src" / "index.html"
        result = read_file(str(path))
        assert result["status"] == "ok"
        assert "<html>" in result["content"]

    def test_read_file_missing(self, tmp_project):
        result = read_file(str(tmp_project / "nonexistent.txt"))
        assert result["status"] == "error"
        assert "not found" in result["error"].lower()

    def test_read_file_directory(self, tmp_project):
        result = read_file(str(tmp_project / "src"))
        assert result["status"] == "error"
        assert "not a file" in result["error"].lower()

    def test_write_file_new(self, tmp_project):
        path = tmp_project / "output" / "test.txt"
        result = write_file(str(path), "hello world")
        assert result["status"] == "ok"
        assert path.read_text() == "hello world"

    def test_write_file_overwrite(self, tmp_project):
        path = tmp_project / "src" / "index.html"
        result = write_file(str(path), "<html><body>Updated</body></html>")
        assert result["status"] == "ok"
        assert "Updated" in path.read_text()

    def test_list_files(self, tmp_project):
        result = list_files(str(tmp_project / "src"))
        assert result["status"] == "ok"
        assert "index.html" in result["files"]

    def test_list_files_with_pattern(self, tmp_project):
        (tmp_project / "src" / "style.css").write_text("body {}")
        result = list_files(str(tmp_project / "src"), "*.html")
        assert result["status"] == "ok"
        assert "index.html" in result["files"]
        assert "style.css" not in result["files"]

    def test_list_files_missing_dir(self, tmp_project):
        result = list_files(str(tmp_project / "nope"))
        assert result["status"] == "error"


class TestPlaywrightTools:
    def test_take_screenshot(self, tmp_project):
        output_path = str(tmp_project / "browser-tests" / "snapshots" / "test.png")
        result = take_screenshot(
            url="http://example.com",
            output_path=output_path,
        )
        assert result["status"] == "ok"
        assert Path(output_path).exists()

    def test_take_screenshot_missing_script(self, tmp_project):
        os.environ["ADK_BROWSER_TESTS_DIR"] = str(tmp_project / "nonexistent")
        result = take_screenshot(url="http://example.com")
        assert result["status"] == "error"
        assert "not found" in result["error"].lower()

    def test_take_screenshot_updates_state(self, tmp_project):
        output_path = str(tmp_project / "browser-tests" / "snapshots" / "test.png")
        mock_ctx = MagicMock()
        mock_ctx.state = {}
        result = take_screenshot(
            url="http://example.com",
            output_path=output_path,
            tool_context=mock_ctx,
        )
        assert result["status"] == "ok"
        assert mock_ctx.state["last_screenshot"] == output_path

    def test_compare_screenshots(self, tmp_project):
        # Create two identical dummy PNGs
        snapshots = tmp_project / "browser-tests" / "snapshots"
        baseline = str(snapshots / "baseline.png")
        current = str(snapshots / "current.png")
        # Write dummy files (validate.js mock doesn't actually read them)
        Path(baseline).write_bytes(b"fake-png")
        Path(current).write_bytes(b"fake-png")

        result = compare_screenshots(baseline, current)
        assert result["status"] == "match"
        assert result["matched"] is True

    def test_compare_screenshots_missing_script(self, tmp_project):
        os.environ["ADK_BROWSER_TESTS_DIR"] = str(tmp_project / "nonexistent")
        result = compare_screenshots("a.png", "b.png")
        assert result["status"] == "error"


class TestLoopControl:
    def test_exit_loop_sets_escalate(self):
        mock_ctx = MagicMock()
        mock_ctx.actions = MagicMock()
        result = exit_loop("all tests pass", tool_context=mock_ctx)
        assert result["status"] == "loop_exited"
        assert result["reason"] == "all tests pass"
        assert mock_ctx.actions.escalate is True
