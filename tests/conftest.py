"""Shared test fixtures for ADK pipeline tests."""

import os
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def tmp_project(tmp_path):
    """Create a minimal mock project structure for testing tools."""
    # Create browser-tests directory structure
    browser_tests = tmp_path / "browser-tests"
    scripts = browser_tests / "scripts"
    snapshots = browser_tests / "snapshots"
    scripts.mkdir(parents=True)
    snapshots.mkdir(parents=True)

    # Create mock screenshot.js that just creates a dummy PNG
    (scripts / "screenshot.js").write_text(
        """
const fs = require('fs');
const args = process.argv.slice(2);
if (args.length < 2) { process.exit(1); }
// Write a minimal 1x1 PNG
const png = Buffer.from(
    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==',
    'base64'
);
fs.writeFileSync(args[1], png);
console.log('Screenshot saved: ' + args[1]);
"""
    )

    # Create mock validate.js that always passes
    (scripts / "validate.js").write_text(
        """
const args = process.argv.slice(2);
if (args.length < 2) { process.exit(1); }
console.log('Pixels compared: 100');
console.log('Pixels different: 0');
console.log('Difference: 0.00%');
console.log('Threshold: 0.1%');
console.log('Result: PASS');
process.exit(0);
"""
    )

    # Create a sample source file
    src = tmp_path / "src"
    src.mkdir()
    (src / "index.html").write_text("<html><body>Hello</body></html>")

    # Point config to this temp project
    os.environ["ADK_BROWSER_TESTS_DIR"] = str(browser_tests)

    yield tmp_path

    # Cleanup
    os.environ.pop("ADK_BROWSER_TESTS_DIR", None)
