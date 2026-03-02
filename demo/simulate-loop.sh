#!/bin/bash

# Simulates a realistic ralph-loop session for demo recording.
# This replays the actual output formats from setup-ralph-loop.sh and stop-hook.sh.

clear

# Colors
BOLD='\033[1m'
DIM='\033[2m'
CYAN='\033[36m'
GREEN='\033[32m'
YELLOW='\033[33m'
RESET='\033[0m'

typeit() {
  local text="$1"
  local delay="${2:-0.035}"
  for (( i=0; i<${#text}; i++ )); do
    printf '%s' "${text:$i:1}"
    sleep "$delay"
  done
}

# --- Prompt ---
sleep 0.3
printf "${BOLD}${CYAN}>${RESET} "
typeit '/ralph-loop "Fix the CSS grid layout" --max-iterations 5 --completion-promise "LAYOUT_FIXED"'
sleep 0.2
echo ""

# --- Setup output (trimmed from scripts/setup-ralph-loop.sh for readability) ---
sleep 0.4
cat <<'EOF'
🔄 Ralph loop activated in this session!

Iteration: 1
Max iterations: 5
Completion promise: LAYOUT_FIXED (ONLY output when TRUE - do not lie!)

The stop hook is now active. When you try to exit, the SAME PROMPT will be
fed back to you, creating a self-referential loop where you iteratively
improve on the same task.

Fix the CSS grid layout

═══════════════════════════════════════════════════════════════
CRITICAL - Ralph Loop Completion Promise
═══════════════════════════════════════════════════════════════
To complete this loop, output this EXACT text:
  <promise>LAYOUT_FIXED</promise>
═══════════════════════════════════════════════════════════════
EOF

# --- Iteration 1: Claude working ---
sleep 1.2
printf "\n${BOLD}Reading${RESET} layout.css...\n"
sleep 0.6
printf "${DIM}  .grid-container { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }${RESET}\n"
sleep 0.5
printf "${BOLD}Running${RESET} test suite...\n"
sleep 0.8
printf "${YELLOW}  2 of 5 tests failing${RESET}\n"
printf "${DIM}  ✗ three-column layout renders correctly${RESET}\n"
printf "${DIM}  ✗ responsive breakpoint at 768px${RESET}\n"

# --- Stop hook iteration 2 (matches hooks/stop-hook.sh line 160) ---
sleep 0.8
echo ""
echo "🔄 Ralph iteration 2 | To stop: output <promise>LAYOUT_FIXED</promise> (ONLY when statement is TRUE - do not lie to exit!)"
echo ""

# --- Iteration 2: Claude working ---
sleep 0.8
printf "${BOLD}Fixing${RESET} grid-template-columns: repeat(3, 1fr)...\n"
sleep 0.5
printf "${BOLD}Adding${RESET} media query for 768px breakpoint...\n"
sleep 0.6
printf "${BOLD}Running${RESET} test suite...\n"
sleep 0.8
printf "${YELLOW}  1 of 5 tests failing${RESET}\n"
printf "${DIM}  ✗ responsive breakpoint at 768px${RESET}\n"

# --- Stop hook iteration 3 ---
sleep 0.8
echo ""
echo "🔄 Ralph iteration 3 | To stop: output <promise>LAYOUT_FIXED</promise> (ONLY when statement is TRUE - do not lie to exit!)"
echo ""

# --- Iteration 3: Claude working ---
sleep 0.8
printf "${BOLD}Adjusting${RESET} breakpoint: grid-template-columns: 1fr at max-width 768px...\n"
sleep 0.6
printf "${BOLD}Running${RESET} test suite...\n"
sleep 1.0
printf "${GREEN}  5 of 5 tests passing${RESET}\n"
sleep 0.5

# --- Promise output ---
printf "\nAll CSS grid tests passing. The layout is fixed.\n"
sleep 0.3
printf "<promise>LAYOUT_FIXED</promise>\n"

# --- Completion (matches hooks/stop-hook.sh line 124) ---
sleep 0.6
echo ""
echo "✅ Ralph loop: Detected <promise>LAYOUT_FIXED</promise>"
sleep 1.5
