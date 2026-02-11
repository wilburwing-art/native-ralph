#!/usr/bin/env bats

load 'test_helper'

SCRIPT_DIR="$(cd "$(dirname "$BATS_TEST_FILENAME")/.." && pwd)"
SETUP_SCRIPT="$SCRIPT_DIR/scripts/setup-ralph-loop.sh"

setup() {
    setup_test_env
}

teardown() {
    teardown_test_env
}

@test "setup script creates state file" {
    run "$SETUP_SCRIPT" "Build a todo app" --max-iterations 10
    [ "$status" -eq 0 ]
    [ -f ".claude/ralph-loop.local.md" ]
}

@test "setup script requires prompt" {
    run "$SETUP_SCRIPT"
    [ "$status" -eq 1 ]
    [[ "$output" == *"No prompt provided"* ]]
}

@test "setup script stores prompt in state file" {
    run "$SETUP_SCRIPT" "Build a REST API" --max-iterations 5
    [ "$status" -eq 0 ]

    content=$(cat .claude/ralph-loop.local.md)
    [[ "$content" == *"Build a REST API"* ]]
}

@test "setup script stores max iterations" {
    run "$SETUP_SCRIPT" "Test task" --max-iterations 25
    [ "$status" -eq 0 ]

    content=$(cat .claude/ralph-loop.local.md)
    [[ "$content" == *"max_iterations: 25"* ]]
}

@test "setup script stores completion promise" {
    run "$SETUP_SCRIPT" "Test task" --completion-promise "COMPLETE" --max-iterations 10
    [ "$status" -eq 0 ]

    content=$(cat .claude/ralph-loop.local.md)
    [[ "$content" == *'completion_promise: "COMPLETE"'* ]]
}

@test "setup script defaults to unlimited iterations" {
    run "$SETUP_SCRIPT" "Test task"
    [ "$status" -eq 0 ]

    content=$(cat .claude/ralph-loop.local.md)
    [[ "$content" == *"max_iterations: 0"* ]]
}

@test "setup script handles multi-word prompts" {
    run "$SETUP_SCRIPT" Build a complete REST API with tests --max-iterations 10
    [ "$status" -eq 0 ]

    content=$(cat .claude/ralph-loop.local.md)
    [[ "$content" == *"Build a complete REST API with tests"* ]]
}

@test "setup script rejects non-numeric max-iterations" {
    run "$SETUP_SCRIPT" "Test" --max-iterations abc
    [ "$status" -eq 1 ]
    [[ "$output" == *"must be a positive integer"* ]]
}

@test "setup script rejects missing max-iterations value" {
    run "$SETUP_SCRIPT" "Test" --max-iterations
    [ "$status" -eq 1 ]
    [[ "$output" == *"requires a number"* ]]
}

@test "setup script shows help with -h" {
    run "$SETUP_SCRIPT" -h
    [ "$status" -eq 0 ]
    [[ "$output" == *"USAGE:"* ]]
}

@test "setup script shows help with --help" {
    run "$SETUP_SCRIPT" --help
    [ "$status" -eq 0 ]
    [[ "$output" == *"Ralph Loop"* ]]
}

@test "setup script initializes iteration to 1" {
    run "$SETUP_SCRIPT" "Test" --max-iterations 10
    [ "$status" -eq 0 ]

    content=$(cat .claude/ralph-loop.local.md)
    [[ "$content" == *"iteration: 1"* ]]
}
