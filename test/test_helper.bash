# Test helper functions for ralph-loop tests

# Set up test environment
setup_test_env() {
    export TEST_DIR="$(mktemp -d)"
    export ORIG_DIR="$(pwd)"
    cd "$TEST_DIR"
    mkdir -p .claude
}

# Tear down test environment
teardown_test_env() {
    cd "$ORIG_DIR"
    rm -rf "$TEST_DIR"
}

# Create a mock state file
create_state_file() {
    local iteration="${1:-1}"
    local max_iterations="${2:-10}"
    local completion_promise="${3:-DONE}"

    cat > .claude/ralph-loop.local.md <<EOF
---
active: true
iteration: $iteration
max_iterations: $max_iterations
completion_promise: "$completion_promise"
started_at: "2024-01-01T00:00:00Z"
---

Test prompt for Ralph loop
EOF
}

# Create mock transcript file
create_transcript() {
    local content="$1"
    local transcript_path="${2:-/tmp/test-transcript.jsonl}"

    # Create JSONL format transcript
    cat > "$transcript_path" <<EOF
{"role":"user","message":{"content":[{"type":"text","text":"test"}]}}
{"role":"assistant","message":{"content":[{"type":"text","text":"$content"}]}}
EOF
    echo "$transcript_path"
}

# Create hook input JSON
create_hook_input() {
    local transcript_path="$1"
    echo "{\"transcript_path\": \"$transcript_path\"}"
}
