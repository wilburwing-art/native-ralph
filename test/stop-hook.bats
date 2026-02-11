#!/usr/bin/env bats

load 'test_helper'

SCRIPT_DIR="$(cd "$(dirname "$BATS_TEST_FILENAME")/.." && pwd)"
STOP_HOOK="$SCRIPT_DIR/hooks/stop-hook.sh"

setup() {
    setup_test_env
}

teardown() {
    teardown_test_env
}

@test "stop hook allows exit when no state file" {
    transcript=$(create_transcript "Hello world")
    input=$(create_hook_input "$transcript")

    run bash -c "echo '$input' | '$STOP_HOOK'"
    [ "$status" -eq 0 ]
    # Should not output block decision
    [[ "$output" != *'"decision": "block"'* ]]
}

@test "stop hook blocks exit when loop active" {
    create_state_file 1 10 "DONE"
    transcript=$(create_transcript "Working on task...")
    input=$(create_hook_input "$transcript")

    run bash -c "echo '$input' | '$STOP_HOOK'"
    [ "$status" -eq 0 ]
    [[ "$output" == *'"decision": "block"'* ]]
}

@test "stop hook increments iteration" {
    create_state_file 3 10 "DONE"
    transcript=$(create_transcript "Still working...")
    input=$(create_hook_input "$transcript")

    echo "$input" | "$STOP_HOOK" > /dev/null

    content=$(cat .claude/ralph-loop.local.md)
    [[ "$content" == *"iteration: 4"* ]]
}

@test "stop hook detects completion promise" {
    create_state_file 1 10 "DONE"
    transcript=$(create_transcript "Task complete! <promise>DONE</promise>")
    input=$(create_hook_input "$transcript")

    run bash -c "echo '$input' | '$STOP_HOOK'"
    [ "$status" -eq 0 ]
    [[ "$output" == *"Detected"* ]]
    # State file should be removed
    [ ! -f ".claude/ralph-loop.local.md" ]
}

@test "stop hook stops at max iterations" {
    create_state_file 10 10 "DONE"
    transcript=$(create_transcript "Working...")
    input=$(create_hook_input "$transcript")

    run bash -c "echo '$input' | '$STOP_HOOK'"
    [ "$status" -eq 0 ]
    [[ "$output" == *"Max iterations"* ]]
    # State file should be removed
    [ ! -f ".claude/ralph-loop.local.md" ]
}

@test "stop hook re-injects original prompt" {
    create_state_file 1 10 "DONE"
    transcript=$(create_transcript "Working on it...")
    input=$(create_hook_input "$transcript")

    output=$(echo "$input" | "$STOP_HOOK")

    # Check that the response contains the original prompt
    [[ "$output" == *"Test prompt for Ralph loop"* ]]
}

@test "stop hook handles missing transcript gracefully" {
    create_state_file 1 10 "DONE"
    input='{"transcript_path": "/nonexistent/path.jsonl"}'

    run bash -c "echo '$input' | '$STOP_HOOK'"
    [ "$status" -eq 0 ]
    [[ "$output" == *"not found"* ]]
    # State file should be removed on error
    [ ! -f ".claude/ralph-loop.local.md" ]
}

@test "stop hook handles corrupted iteration" {
    # Create state file with non-numeric iteration
    cat > .claude/ralph-loop.local.md <<'EOF'
---
active: true
iteration: abc
max_iterations: 10
completion_promise: "DONE"
---

Test prompt
EOF

    transcript=$(create_transcript "test")
    input=$(create_hook_input "$transcript")

    run bash -c "echo '$input' | '$STOP_HOOK'"
    [ "$status" -eq 0 ]
    [[ "$output" == *"corrupted"* ]]
}

@test "stop hook includes iteration in system message" {
    create_state_file 5 10 "DONE"
    transcript=$(create_transcript "Working...")
    input=$(create_hook_input "$transcript")

    output=$(echo "$input" | "$STOP_HOOK")

    [[ "$output" == *"iteration 6"* ]]
}

@test "stop hook runs infinitely when max_iterations is 0" {
    create_state_file 100 0 "DONE"
    transcript=$(create_transcript "Still going...")
    input=$(create_hook_input "$transcript")

    run bash -c "echo '$input' | '$STOP_HOOK'"
    [ "$status" -eq 0 ]
    [[ "$output" == *'"decision": "block"'* ]]
}
