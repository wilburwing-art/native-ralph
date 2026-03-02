#!/usr/bin/env bash
set -euo pipefail

# Bridge script: runs the ADK UI refinement pipeline via uv.
# Called from the /adk-loop slash command.
#
# Usage: run-adk-pipeline.sh [--url URL] [--max-iterations N]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

URL="http://localhost:3000"
MAX_ITERATIONS=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --url)
            URL="$2"
            shift 2
            ;;
        --max-iterations)
            MAX_ITERATIONS="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: run-adk-pipeline.sh [--url URL] [--max-iterations N]"
            echo ""
            echo "Options:"
            echo "  --url URL              Target URL (default: http://localhost:3000)"
            echo "  --max-iterations N     Max refinement iterations (default: 5)"
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

cd "$PROJECT_ROOT"

CMD=(uv run -m adk_agents --url "$URL")
if [[ -n "$MAX_ITERATIONS" ]]; then
    CMD+=(--max-iterations "$MAX_ITERATIONS")
fi

echo "Running ADK pipeline targeting $URL..."
exec "${CMD[@]}"
