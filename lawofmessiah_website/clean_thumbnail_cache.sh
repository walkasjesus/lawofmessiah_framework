#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

if [[ -x "$SCRIPT_DIR/venv/bin/python3" ]]; then
	PYTHON_BIN="$SCRIPT_DIR/venv/bin/python3"
elif [[ -x "$SCRIPT_DIR/venv/bin/python" ]]; then
	PYTHON_BIN="$SCRIPT_DIR/venv/bin/python"
elif [[ -x "$SCRIPT_DIR/../venv/bin/python3" ]]; then
	PYTHON_BIN="$SCRIPT_DIR/../venv/bin/python3"
elif [[ -x "$SCRIPT_DIR/../venv/bin/python" ]]; then
	PYTHON_BIN="$SCRIPT_DIR/../venv/bin/python"
else
	PYTHON_BIN="python3"
fi

if command -v tee >/dev/null 2>&1 && command -v date >/dev/null 2>&1; then
	today=$(date +%Y%m%d)
	start=$(date '+%Y-%m-%d %H:%M:%S')
	log="log/install.${today}.log"
	log_cmd=(tee -a "$log")
else
	start=""
	log_cmd=(cat)
fi

echo "INFO: ${start} - Start cleaning thumbnail caches" | "${log_cmd[@]}"
"$PYTHON_BIN" manage.py thumbnail cleanup | "${log_cmd[@]}"

if command -v date >/dev/null 2>&1; then
	end=$(date '+%Y-%m-%d %H:%M:%S')
	echo "INFO: ${end} - Ended cleaning thumbnail caches" | "${log_cmd[@]}"
else
	echo "INFO: Ended cleaning thumbnail caches" | "${log_cmd[@]}"
fi
