#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[1;34m'
YELLOW='\033[1;33m'
RESET='\033[0m'

dir=$(basename "$(pwd)")

for command in \
    "uv run --exact -- ruff check --fix --quiet" \
    "uv run --exact -- ruff format --quiet" \
    "uv run --exact -- pyright" \
    "uv run --exact -- pytest -vv" \
; do
    if eval "$command"; then
        echo -e "${GREEN}✔${RESET} ${BLUE}[$dir]${RESET} $command"
    else
        exit_status=$?
        echo -e "${RED}✘${RESET} ${BLUE}[$dir]${RESET} $command failed with exit code ${exit_status}" >&2
        exit $exit_status
    fi
done
